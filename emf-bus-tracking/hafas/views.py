import enum
import json
import secrets
import dataclasses
import traceback
import datetime
import typing
import uuid
import decimal
import xsdata.formats.dataclass.serializers.xml
import xsdata.formats.dataclass.serializers.json
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.core.cache import cache
import tracking.models
import darwin.models
from . import hafas_rest


class DataFormat(enum.Enum):
    XML = "xml"
    JSON = "json"


class Language(enum.Enum):
    English = "en"
    Welsh = "cy"


@dataclasses.dataclass
class RequestContext:
    data_format: DataFormat
    language: Language
    request_id: str
    request_data: dict
    request_time: datetime.datetime


def encode_json_value(val):
    if isinstance(val, enum.Enum):
        return val.value
    elif isinstance(val, decimal.Decimal):
        return str(val)
    else:
        return val


def encode_json(obj):
    if not dataclasses.is_dataclass(obj):
        return {"value": encode_json_value(obj)}

    out = {}
    fields = dataclasses.fields(obj)

    for field in fields:
        value = getattr(obj, field.name)
        if value is not None:
            field_type = field.metadata.get("type", None)
            field_name = field.metadata.get("name", field.name)
            if field_type == "Element":
                if isinstance(value, list):
                    out[field_name] = [encode_json(v) for v in value]
                else:
                    out[field_name] = encode_json(value)
            elif field_type == "Attribute":
                out[field_name] = encode_json_value(value)
            else:
                out["value"] = encode_json_value(value)

    return out


def hafas_request(wrapped):
    def handler(request):
        if request.method == "POST":
            request_data = dict(request.POST)
        else:
            request_data = dict(request.GET)

        request_data = {k: v[0] for k, v in request_data.items() if v}

        context = RequestContext(
            data_format=DataFormat.XML,
            language=Language.English,
            request_id=secrets.token_hex(8),
            request_data=request_data,
            request_time=timezone.now(),
        )

        if request_format := request_data.pop("format", None):
            if request_format == "json":
                context.data_format = DataFormat.JSON
            elif request_format == "xml":
                context.data_format = DataFormat.XML
            else:
                return HttpResponse(status=400)
        else:
            if request.accepts("application/xml"):
                context.data_format = DataFormat.XML
            elif request.accepts("application/json"):
                context.data_format = DataFormat.JSON
            else:
                return HttpResponse(status=406)

        if request_id := request_data.pop("requestId", None):
            context.request_id = request_id

        if language := request_data.pop("lang", None):
            try:
                context.language = Language(language)
            except ValueError:
                return HttpResponse(status=400)

        try:
            response: hafas_rest.CommonResponseType = wrapped(context)
        except Exception as e:
            traceback.print_exception(e)
            response = hafas_rest.CommonResponseType(
                error_code="500",
                error_text="Internal Server Error",
            )

        response.request_id = context.request_id

        if not response.technical_messages:
            response.technical_messages = hafas_rest.TechnicalMessages()

        response.technical_messages.technical_message.append(hafas_rest.TechnicalMessage(
            key="requestTime",
            value=context.request_time.isoformat()
        ))

        unmapped_params = list(context.request_data.keys())
        if unmapped_params:
            response.technical_messages.technical_message.append(hafas_rest.TechnicalMessage(
                key="unmappedQueryParams",
                value=",".join(unmapped_params)
            ))

        if context.data_format == DataFormat.XML:
            serializer = xsdata.formats.dataclass.serializers.xml.XmlSerializer()
            resp_text = serializer.render(response)

            return HttpResponse(resp_text, content_type="application/xml")
        elif context.data_format == DataFormat.JSON:
            resp_text = json.dumps(encode_json(response))

            return HttpResponse(resp_text, content_type="application/json")

    return handler


@hafas_request
def location_search_by_name(request_context: RequestContext) -> hafas_rest.CommonResponseType:
    search_input = request_context.request_data.pop("input", None)
    if not search_input:
        return hafas_rest.CommonResponseType(
            error_code="400",
            error_text="Missing input",
        )

    search_results = tracking.models.Stop.objects.filter(name__icontains=search_input)

    location_list = []

    for location in search_results:
        darwin_location = location.darwin_link.first()
        location_list.append(hafas_rest.StopLocation(
            name=location.name,
            id=str(location.id),
            ext_id=f"tiploc:{darwin_location.location_id}" if darwin_location else None,
            lon=decimal.Decimal(location.longitude),
            lat=decimal.Decimal(location.latitude),
            links=[hafas_rest.ResourceLinks(
                link=[hafas_rest.ResourceLinkType(
                    rel="self",
                    href=location.url
                )]
            )] if location.url else None
        ))

    return hafas_rest.LocationList(stop_location=location_list)


def board_common(wrapped):
    def inner(request_context: RequestContext):
        now = timezone.now().astimezone(datetime.UTC)

        stop_id = request_context.request_data.pop("id", None)
        if not stop_id:
            return hafas_rest.CommonResponseType(
                error_code="400",
                error_text="Missing id",
            )

        try:
            stop_id = uuid.UUID(stop_id)
        except ValueError:
            return hafas_rest.CommonResponseType(
                error_code="400",
                error_text=f"Invalid id: {stop_id}",
            )
        stop_obj: tracking.models.Stop = tracking.models.Stop.objects.filter(id=stop_id).first()
        if not stop_obj:
            return hafas_rest.CommonResponseType(
                error_code="404",
                error_text=f"Stop not found: {stop_id}",
            )

        date = request_context.request_data.pop("date", None)
        if not date:
            search_date = now.date()
        else:
            try:
                search_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return hafas_rest.CommonResponseType(
                    error_code="400",
                    error_text=f"Invalid date: {date}",
                )

        time = request_context.request_data.pop("time", None)
        if not time:
            search_time = now.time()
        else:
            try:
                search_time = datetime.datetime.strptime(time, "%H:%M:%S").time()
            except ValueError:
                return hafas_rest.CommonResponseType(
                    error_code="400",
                    error_text=f"Invalid time: {time}",
                )

        search_minutes = 60
        if duration := request_context.request_data.pop("duration", None):
            try:
                search_minutes = min(int(duration), 1439)
            except ValueError:
                return hafas_rest.CommonResponseType(
                    error_code="400",
                    error_text=f"Invalid duration: {duration}",
                )

        search_lines = []
        if lines := request_context.request_data.pop("lines", None):
            for line_id in lines.split(","):
                negative_search = False
                if line_id.startswith("!"):
                    negative_search = True

                try:
                    line_id = uuid.UUID(line_id)
                except ValueError:
                    return hafas_rest.CommonResponseType(
                        error_code="400",
                        error_text=f"Invalid id: {line_id}",
                    )
                line = tracking.models.Route.objects.filter(id=line_id).first()
                if not line:
                    return hafas_rest.CommonResponseType(
                        error_code="404",
                        error_text=f"Line not found: {line_id}",
                    )
                search_lines.append((line, negative_search))

        search_start_time = datetime.datetime.combine(search_date, search_time).replace(tzinfo=datetime.UTC)
        search_end_time = search_start_time + datetime.timedelta(minutes=search_minutes)
        search_start_time -= datetime.timedelta(minutes=5)

        return wrapped(request_context, stop_obj, search_start_time, search_end_time, search_lines)

    return inner


@hafas_request
@board_common
def arrival_board(
        request_context: RequestContext,
        stop_obj: tracking.models.Stop,
        search_start_time: datetime.datetime,
        search_end_time: datetime.datetime,
        search_lines: typing.List[typing.Tuple[tracking.models.Route, bool]]
) -> hafas_rest.CommonResponseType:
    arrival_board_elements = []

    def filter_tracking_journey_stop(stop: tracking.models.JourneyPoint):
        if stop.real_time_arrival:
            return search_start_time <= stop.real_time_arrival <= search_end_time
        elif stop.estimated_arrival:
            return search_start_time <= stop.estimated_arrival <= search_end_time
        elif stop.arrival_time:
            return search_start_time <= stop.arrival_time <= search_end_time
        else:
            return False

    def filter_darwin_journey_stop(stop: darwin.models.JourneyStop):
        if stop.actual_arrival:
            return search_start_time <= stop.actual_arrival <= search_end_time
        elif stop.estimated_arrival:
            return search_start_time <= stop.estimated_arrival <= search_end_time
        elif stop.public_arrival:
            return search_start_time <= stop.public_arrival <= search_end_time
        else:
            return False

    relevant_journey_stops = stop_obj.journey_points.filter(
        Q(journey__public=True) & (
                Q(arrival_time__gte=search_start_time) |
                Q(estimated_arrival__gte=search_start_time) |
                Q(real_time_arrival__gte=search_start_time)
        ) & (
                Q(arrival_time__lte=search_end_time) |
                Q(estimated_arrival__lte=search_end_time) |
                Q(real_time_arrival__lte=search_end_time)
        )
    )
    relevant_journey_stops: typing.List[tracking.models.JourneyPoint] = \
        list(filter(filter_tracking_journey_stop, relevant_journey_stops))
    for journey_stop in relevant_journey_stops:
        if not journey_stop.arrival_time:
            continue

        rt_arrival = journey_stop.real_time_arrival.astimezone(datetime.UTC) or \
                     journey_stop.estimated_arrival.astimezone(datetime.UTC) or None
        origin_stop: typing.Optional[tracking.models.JourneyPoint] = \
            journey_stop.journey.points.order_by("order").first()

        arrival_board_elements.append((journey_stop.arrival_time, hafas_rest.Arrival(
            name=journey_stop.journey.code,
            type_value=hafas_rest.ArrivalType.ST,
            tz=0,
            rt_tz=0,
            stop=journey_stop.stop.name,
            stopid=str(stop_obj.id),
            lon=decimal.Decimal(stop_obj.longitude),
            lat=decimal.Decimal(stop_obj.latitude),

            date=journey_stop.arrival_time.astimezone(datetime.UTC).date().isoformat(),
            time=journey_stop.arrival_time.astimezone(datetime.UTC).time().isoformat(),

            rt_date=rt_arrival.date().isoformat() if rt_arrival else None,
            rt_time=rt_arrival.time().isoformat() if rt_arrival else None,

            cancelled=journey_stop.journey.real_time_state == tracking.models.Journey.RT_STATE_CANCELLED,

            origin=origin_stop.stop.name if origin_stop else None,

            product=[journey_to_product(journey_stop)],

            stops=hafas_rest.Stops(
                stop=[stop_to_hafas(s) for s in journey_stop.journey.points.filter(
                    order__lte=journey_stop.order
                )]
            ),

            journey_detail_ref=hafas_rest.JourneyDetailRef(
                ref=f"own:{journey_stop.journey.id}"
            ),

            notes=hafas_rest.Notes()
        )))

    for darwin_location in stop_obj.darwin_link.all():
        darwin_location = darwin_location.location()
        if not darwin_location:
            continue

        darwin_relevant_journey_stops = darwin.models.JourneyStop.objects.filter(
            Q(location=darwin_location) & (
                    Q(public_arrival__gte=search_start_time) |
                    Q(estimated_arrival__gte=search_start_time) |
                    Q(actual_arrival__gte=search_start_time)
            ) & (
                    Q(public_arrival__lte=search_end_time) |
                    Q(estimated_arrival__lte=search_end_time) |
                    Q(actual_arrival__lte=search_end_time)
            )
        )

        darwin_relevant_journey_stops: typing.List[darwin.models.JourneyStop] = \
            list(filter(filter_darwin_journey_stop, darwin_relevant_journey_stops))

        for journey_stop in darwin_relevant_journey_stops:
            if not journey_stop.public_arrival:
                continue

            rt_arrival = journey_stop.actual_arrival or journey_stop.estimated_arrival or None
            part_cancelled = any(
                s.cancelled for s in darwin.models.JourneyStop.objects.filter(journey_id=journey_stop.journey_id))
            origin_stop: typing.Optional[darwin.models.JourneyStop] = darwin.models.JourneyStop.objects.filter(
                journey_id=journey_stop.journey_id, origin=True).first()
            journey = darwin.models.Journey.objects.filter(rtti_unique_id=journey_stop.journey_id).first()

            arrival_board_elements.append((journey_stop.public_arrival, hafas_rest.Arrival(
                name=journey_stop.journey.headcode,
                type_value=hafas_rest.ArrivalType.ST,
                tz=0,
                rt_tz=0,
                stop=get_location_name(request_context, journey_stop.location_id),
                stopid=str(stop_obj.id),
                stop_ext_id=f"tiploc:{journey_stop.location_id}",
                lon=decimal.Decimal(stop_obj.longitude),
                lat=decimal.Decimal(stop_obj.latitude),

                date=journey_stop.public_arrival.astimezone(datetime.UTC).date().isoformat(),
                time=journey_stop.public_arrival.astimezone(datetime.UTC).time().isoformat(),

                rt_date=rt_arrival.astimezone(datetime.UTC).date().isoformat() if rt_arrival else None,
                rt_time=rt_arrival.astimezone(datetime.UTC).time().isoformat() if rt_arrival else None,

                platform=hafas_rest.PlatformType(
                    type_value=hafas_rest.PlatformTypeType.PL,
                    text=journey_stop.planned_platform,
                    hidden=journey_stop.platform_suppressed,
                ) if journey_stop.planned_platform else None,
                rt_platform=hafas_rest.PlatformType(
                    type_value=hafas_rest.PlatformTypeType.PL,
                    text=journey_stop.current_platform,
                    hidden=journey_stop.platform_suppressed,
                ) if journey_stop.current_platform else None,

                cancelled=journey.cancel_reason_id is not None,
                part_cancelled=part_cancelled,

                origin=get_location_name(request_context, origin_stop.location_id) if origin_stop else None,

                uncertain_delay=journey_stop.unknown_delay_departure,

                product=[darwin_journey_to_product(request_context, journey)],

                stops=hafas_rest.Stops(
                    stop=[darwin_stop_to_hafas(request_context, s) for s in darwin.models.JourneyStop.objects.filter(
                        journey_id=journey_stop.journey_id, order__lte=journey_stop.order
                    )]
                ),

                journey_detail_ref=hafas_rest.JourneyDetailRef(
                    ref=f"darwin:{journey.rtti_unique_id}"
                ),

                notes=darwin_hafas_notes(request_context, journey)
            )))

    arrival_board_elements.sort(key=lambda x: x[0])
    arrival_board_output = hafas_rest.ArrivalBoard(arrival=[
        e[1] for e in arrival_board_elements
    ])
    return arrival_board_output


@hafas_request
@board_common
def departure_board(
        request_context: RequestContext,
        stop_obj: tracking.models.Stop,
        search_start_time: datetime.datetime,
        search_end_time: datetime.datetime,
        search_lines: typing.List[typing.Tuple[tracking.models.Route, bool]]
) -> hafas_rest.CommonResponseType:
    departure_board_elements = []

    def filter_tracking_journey_stop(stop: tracking.models.JourneyPoint):
        if stop.real_time_departure:
            return search_start_time <= stop.real_time_departure <= search_end_time
        elif stop.estimated_departure:
            return search_start_time <= stop.estimated_departure <= search_end_time
        elif stop.departure_time:
            return search_start_time <= stop.departure_time <= search_end_time
        else:
            return False

    def filter_journey_stop(stop: darwin.models.JourneyStop):
        if stop.actual_departure:
            return search_start_time <= stop.actual_departure <= search_end_time
        elif stop.estimated_departure:
            return search_start_time <= stop.estimated_departure <= search_end_time
        elif stop.public_departure:
            return search_start_time <= stop.public_departure <= search_end_time
        else:
            return False

    relevant_journey_stops = stop_obj.journey_points.filter(
        Q(journey__public=True) & (
                Q(departure_time__gte=search_start_time) |
                Q(estimated_departure__gte=search_start_time) |
                Q(real_time_departure__gte=search_start_time)
        ) & (
                Q(departure_time__lte=search_end_time) |
                Q(estimated_departure__lte=search_end_time) |
                Q(real_time_departure__lte=search_end_time)
        )
    )
    relevant_journey_stops: typing.List[tracking.models.JourneyPoint] = \
        list(filter(filter_tracking_journey_stop, relevant_journey_stops))
    for journey_stop in relevant_journey_stops:
        if not journey_stop.departure_time:
            continue

        rt_departure = journey_stop.real_time_departure or \
                     journey_stop.estimated_departure or None
        destination_stop: typing.Optional[tracking.models.JourneyPoint] = \
            journey_stop.journey.points.order_by("-order").first()

        departure_board_elements.append((journey_stop.departure_time, hafas_rest.Departure(
            name=journey_stop.journey.code,
            type_value=hafas_rest.DepartureType.ST,
            tz=0,
            rt_tz=0,
            stop=journey_stop.stop.name,
            stopid=str(stop_obj.id),
            lon=decimal.Decimal(stop_obj.longitude),
            lat=decimal.Decimal(stop_obj.latitude),

            date=journey_stop.departure_time.astimezone(datetime.UTC).date().isoformat(),
            time=journey_stop.departure_time.astimezone(datetime.UTC).time().isoformat(),

            rt_date=rt_departure.astimezone(datetime.UTC).date().isoformat() if rt_departure else None,
            rt_time=rt_departure.astimezone(datetime.UTC).time().isoformat() if rt_departure else None,

            cancelled=journey_stop.journey.real_time_state == tracking.models.Journey.RT_STATE_CANCELLED,

            direction=destination_stop.stop.name if destination_stop else None,

            product=[journey_to_product(journey_stop)],

            stops=hafas_rest.Stops(
                stop=[stop_to_hafas(s) for s in journey_stop.journey.points.filter(
                    order__lte=journey_stop.order
                )]
            ),

            journey_detail_ref=hafas_rest.JourneyDetailRef(
                ref=f"own:{journey_stop.journey.id}"
            ),

            notes=hafas_rest.Notes()
        )))

    for darwin_location in stop_obj.darwin_link.all():
        darwin_location = darwin_location.location()
        if not darwin_location:
            continue

        darwin_relevant_journey_stops = darwin.models.JourneyStop.objects.filter(
            Q(location=darwin_location) & (
                    Q(public_departure__gte=search_start_time) |
                    Q(estimated_departure__gte=search_start_time) |
                    Q(actual_departure__gte=search_start_time)
            ) & (
                    Q(public_departure__lte=search_end_time) |
                    Q(estimated_departure__lte=search_end_time) |
                    Q(actual_departure__lte=search_end_time)
            )
        )

        darwin_relevant_journey_stops: typing.List[darwin.models.JourneyStop] = \
            list(filter(filter_journey_stop, darwin_relevant_journey_stops))

        for journey_stop in darwin_relevant_journey_stops:
            if not journey_stop.public_departure:
                continue

            rt_departure = journey_stop.actual_departure or journey_stop.estimated_departure or None
            part_cancelled = any(
                s.cancelled for s in darwin.models.JourneyStop.objects.filter(journey_id=journey_stop.journey_id))
            destination_stop: typing.Optional[darwin.models.JourneyStop] = darwin.models.JourneyStop.objects.filter(
                journey_id=journey_stop.journey_id, destination=True).first()
            journey = darwin.models.Journey.objects.filter(rtti_unique_id=journey_stop.journey_id).first()

            destination_arrival = (
                    destination_stop.actual_arrival or destination_stop.estimated_arrival or None
            ) if destination_stop else None

            departure_board_elements.append((journey_stop.public_departure, hafas_rest.Departure(
                name=journey_stop.journey.headcode,
                type_value=hafas_rest.DepartureType.ST,
                tz=0,
                rt_tz=0,
                stop=get_location_name(request_context, journey_stop.location_id),
                stopid=str(stop_obj.id),
                stop_ext_id=f"tiploc:{journey_stop.location_id}",
                lon=decimal.Decimal(stop_obj.longitude),
                lat=decimal.Decimal(stop_obj.latitude),

                date=journey_stop.public_departure.date().isoformat(),
                time=journey_stop.public_departure.time().isoformat(),

                rt_date=rt_departure.astimezone(datetime.UTC).date().isoformat() if rt_departure else None,
                rt_time=rt_departure.astimezone(datetime.UTC).time().isoformat() if rt_departure else None,

                platform=hafas_rest.PlatformType(
                    type_value=hafas_rest.PlatformTypeType.PL,
                    text=journey_stop.planned_platform,
                    hidden=journey_stop.platform_suppressed,
                ) if journey_stop.planned_platform else None,
                rt_platform=hafas_rest.PlatformType(
                    type_value=hafas_rest.PlatformTypeType.PL,
                    text=journey_stop.current_platform,
                    hidden=journey_stop.platform_suppressed,
                ) if journey_stop.current_platform else None,

                cancelled=journey.cancel_reason_id is not None,
                part_cancelled=part_cancelled,

                direction=get_location_name(request_context,
                                            destination_stop.location_id) if destination_stop else None,
                direction_ext_id=f"tiploc:{destination_stop.location_id}" if destination_stop else None,

                date_at_arrival=destination_stop.public_arrival.date().isoformat() if destination_stop else None,
                time_at_arrival=destination_stop.public_arrival.time().isoformat() if destination_stop else None,

                rt_date_at_arrival=destination_arrival.date().isoformat() if destination_arrival else None,
                rt_time_at_arrival=destination_arrival.time().isoformat() if destination_arrival else None,

                uncertain_delay=journey_stop.unknown_delay_departure,

                product=[darwin_journey_to_product(request_context, journey)],

                stops=hafas_rest.Stops(
                    stop=[darwin_stop_to_hafas(request_context, s) for s in darwin.models.JourneyStop.objects.filter(
                        journey_id=journey_stop.journey_id, order__gt=journey_stop.order
                    )]
                ),

                journey_detail_ref=hafas_rest.JourneyDetailRef(
                    ref=f"darwin:{journey.rtti_unique_id}"
                ),

                notes=darwin_hafas_notes(request_context, journey)
            )))

    departure_board_elements.sort(key=lambda x: x[0])
    departure_board_output = hafas_rest.DepartureBoard(departure=[
        e[1] for e in departure_board_elements
    ])
    return departure_board_output


def darwin_stop_to_hafas(request_context: RequestContext, stop: darwin.models.JourneyStop) -> hafas_rest.StopType:
    own_stop_id_cache_key = f"darwin_stop_id:{stop.location_id}"
    own_stop = None
    if own_stop_id := cache.get(own_stop_id_cache_key) is not None:
        if own_stop_id != "NONE":
            own_stop = tracking.models.Stop.objects.filter(id=own_stop_id).first()
    else:
        darwin_location = darwin.models.Location.objects.filter(tiploc=stop.location_id).first()
        monitored_stop = darwin.models.MonitoredStation.objects.filter(crs=darwin_location.crs).first()
        own_stop: typing.Optional[tracking.models.Stop] = monitored_stop.linked_stop if monitored_stop else None
        cache.set(own_stop_id_cache_key, own_stop.id if own_stop else "NONE", 3600)

    rt_arrival = stop.actual_departure or stop.estimated_departure or None
    rt_departure = stop.actual_departure or stop.estimated_departure or None

    return hafas_rest.StopType(
        id=str(own_stop.id) if own_stop else None,
        name=get_location_name(request_context, stop.location_id),
        ext_id=f"tiploc:{stop.location_id}",
        lon=decimal.Decimal(own_stop.longitude) if own_stop else None,
        lat=decimal.Decimal(own_stop.latitude) if own_stop else None,
        dep_tz=0,
        arr_tz=0,
        rt_dep_tz=0,
        rt_arr_tz=0,

        dep_date=stop.public_departure.astimezone(datetime.UTC).date().isoformat() if stop.public_departure else None,
        dep_time=stop.public_departure.astimezone(datetime.UTC).time().isoformat() if stop.public_departure else None,

        arr_date=stop.public_arrival.astimezone(datetime.UTC).date().isoformat() if stop.public_arrival else None,
        arr_time=stop.public_arrival.astimezone(datetime.UTC).time().isoformat() if stop.public_arrival else None,

        rt_dep_date=rt_departure.astimezone(datetime.UTC).date().isoformat() if rt_departure else None,
        rt_dep_time=rt_departure.astimezone(datetime.UTC).time().isoformat() if rt_departure else None,

        rt_arr_date=rt_arrival.astimezone(datetime.UTC).date().isoformat() if rt_arrival else None,
        rt_arr_time=rt_arrival.astimezone(datetime.UTC).time().isoformat() if rt_arrival else None,

        arr_uncertain_delay=stop.unknown_delay_arrival,
        dep_uncertain_delay=stop.unknown_delay_departure,

        cancelled=stop.cancelled,

        dep_platform=hafas_rest.PlatformType(
            type_value=hafas_rest.PlatformTypeType.PL,
            text=stop.planned_platform,
            hidden=stop.platform_suppressed,
        ) if stop.planned_platform else None,
        arr_platform=hafas_rest.PlatformType(
            type_value=hafas_rest.PlatformTypeType.PL,
            text=stop.planned_platform,
            hidden=stop.platform_suppressed,
        ) if stop.planned_platform else None,

        rt_arr_platform=hafas_rest.PlatformType(
            type_value=hafas_rest.PlatformTypeType.PL,
            text=stop.current_platform,
            hidden=stop.platform_suppressed,
        ) if stop.current_platform else None,
        rt_dep_platform=hafas_rest.PlatformType(
            type_value=hafas_rest.PlatformTypeType.PL,
            text=stop.current_platform,
            hidden=stop.platform_suppressed,
        ) if stop.current_platform else None,

        notes=hafas_rest.Notes()
    )


def darwin_journey_to_product(
        request_context: RequestContext, journey: darwin.models.Journey
) -> hafas_rest.ProductType:
    product = hafas_rest.ProductType(
        operator_info=hafas_rest.OperatorType(
            name=get_toc_name(request_context, journey.toc_id),
            id=journey.toc_id,
        ),
        operator_code=journey.toc_id,
        name=journey.headcode,
    )

    if category := journey.map_service_category():
        product.cat_code = category.value
        product.cat_out = category.name()

    return product


def darwin_hafas_notes(request_context: RequestContext, journey: darwin.models.Journey) -> hafas_rest.Notes:
    notes = hafas_rest.Notes()

    if journey.cancel_reason_id:
        cancel_reason_key = f"darwin_cancel_reason:{journey.cancel_reason_id}"
        if cancel_reason := cache.get(cancel_reason_key):
            text = cancel_reason
        else:
            text = journey.cancel_reason.description
            cache.set(cancel_reason_key, text)

        if journey.cancel_location_id:
            location_name = get_location_name(request_context, journey.cancel_location_id)
            if location_name:
                if journey.cancel_reason_near:
                    text = f"{text} near {location_name}"
                else:
                    text = f"{text} at {location_name}"

        notes.note.append(hafas_rest.Note(
            key="cancelReason",
            type_value=hafas_rest.NoteType.P,
            value=text,
        ))

    elif journey.late_reason_id:
        late_reason_key = f"darwin_late_reason:{journey.late_reason_id}"
        if late_reason := cache.get(late_reason_key):
            text = late_reason
        else:
            text = journey.late_reason.description
            cache.set(late_reason_key, text)

        if journey.late_location_id:
            location_name = get_location_name(request_context, journey.late_location_id)
            if location_name:
                if journey.late_reason_near:
                    text = f"{text} near {location_name}"
                else:
                    text = f"{text} at {location_name}"

        notes.note.append(hafas_rest.Note(
            key="lateReason",
            type_value=hafas_rest.NoteType.D,
            value=text,
        ))

    return notes


def get_location_name(request_context: RequestContext, tiploc: str) -> typing.Optional[str]:
    cache_key = f"darwin_location_name:{tiploc}"
    if name := cache.get(cache_key):
        return name
    
    name = None
    location = darwin.models.Location.objects.filter(tiploc=tiploc).first()
    if location:
        if request_context.language == Language.Welsh and location.crs:
            welsh_name = darwin.models.WelshStationName.objects.filter(crs=location.crs).first()
            if welsh_name:
                name = welsh_name.name
        
        if not name:
            name = location.name

    cache.set(cache_key, name)
    return name


def get_toc_name(request_context: RequestContext, toc_code: str) -> typing.Optional[str]:
    cache_key = f"darwin_toc_name:{toc_code}"
    if name := cache.get(cache_key):
        return name

    name = None
    toc = darwin.models.TrainOperatingCompany.objects.filter(code=toc_code).first()
    if toc:
        if request_context.language == Language.Welsh:
            welsh_name = darwin.models.WelshTrainOperatingCompanyName.objects.filter(toc=toc).first()
            if welsh_name:
                name =  welsh_name.name

        if not name:
            name = toc.name

    cache.set(cache_key, name)
    return name


def journey_to_product(journey_stop: tracking.models.JourneyPoint) -> hafas_rest.ProductType:
    product = hafas_rest.ProductType(
        operator_info=hafas_rest.OperatorType(
            name=settings.TRANSIT_CONFIG["agency_name"],
            id=settings.TRANSIT_CONFIG["agency_id"]
        ),
        operator_code=settings.TRANSIT_CONFIG["agency_id"],
        name=journey_stop.journey.code,
    )

    if journey_stop.journey.route:
        product.icon = hafas_rest.IconType(
            background_color=hafas_rest.RgbacolorType(
                hex=journey_stop.journey.route.color
            ),
            foreground_color=hafas_rest.RgbacolorType(
                hex=journey_stop.journey.route.text_color
            ),
            txt=journey_stop.journey.route.name
        )
        category = journey_stop.journey.route.service_category()
        product.cat_code = category.value
        product.cat_out = category.name()

    return product


def stop_to_hafas(journey_stop: tracking.models.JourneyPoint) -> hafas_rest.StopType:
    rt_arrival = journey_stop.real_time_arrival or journey_stop.estimated_arrival or None
    rt_departure = journey_stop.real_time_departure or journey_stop.estimated_departure or None

    return hafas_rest.StopType(
        id=str(journey_stop.stop.id),
        name=journey_stop.stop.name,
        lon=decimal.Decimal(journey_stop.stop.longitude),
        lat=decimal.Decimal(journey_stop.stop.latitude),
        dep_tz=0,
        arr_tz=0,
        rt_dep_tz=0,
        rt_arr_tz=0,

        dep_date=journey_stop.departure_time.astimezone(datetime.UTC).date().isoformat()
        if journey_stop.departure_time else None,
        dep_time=journey_stop.departure_time.astimezone(datetime.UTC).time().isoformat()
        if journey_stop.departure_time else None,

        arr_date=journey_stop.arrival_time.astimezone(datetime.UTC).date().isoformat()
        if journey_stop.arrival_time else None,
        arr_time=journey_stop.arrival_time.astimezone(datetime.UTC).time().isoformat()
        if journey_stop.arrival_time else None,

        rt_dep_date=rt_departure.astimezone(datetime.UTC).date().isoformat() if rt_departure else None,
        rt_dep_time=rt_departure.astimezone(datetime.UTC).time().isoformat() if rt_departure else None,

        rt_arr_date=rt_arrival.astimezone(datetime.UTC).date().isoformat() if rt_arrival else None,
        rt_arr_time=rt_arrival.astimezone(datetime.UTC).time().isoformat() if rt_arrival else None,

        notes=hafas_rest.Notes()
    )
