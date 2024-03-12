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
def departure_board(request_context: RequestContext) -> hafas_rest.CommonResponseType:
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

    departure_board_elements = []

    def filter_journey_stop(stop: darwin.models.JourneyStop):
        if stop.actual_departure:
            return search_start_time <= stop.actual_departure <= search_end_time
        elif stop.estimated_departure:
            return search_start_time <= stop.estimated_departure <= search_end_time
        elif stop.public_departure:
            return search_start_time <= stop.public_departure <= search_end_time
        else:
            return False

    for darwin_location in stop_obj.darwin_link.all():
        darwin_location = darwin_location.location()
        if not darwin_location:
            continue

        relevant_journey_stops = darwin.models.JourneyStop.objects.filter(
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

        relevant_journey_stops: typing.List[darwin.models.JourneyStop] = \
            list(filter(filter_journey_stop, relevant_journey_stops))

        for journey_stop in relevant_journey_stops:
            if not journey_stop.public_departure:
                continue
                
            rt_departure = journey_stop.actual_departure or journey_stop.estimated_departure or None
            part_cancelled = any(s.cancelled for s in journey_stop.journey.stops.all())
            destination_stop: typing.Optional[darwin.models.JourneyStop] = \
                journey_stop.journey.stops.filter(destination=True).first()

            destination_arrival = (
                    destination_stop.actual_arrival or destination_stop.estimated_arrival or None
            ) if destination_stop else None

            product = hafas_rest.ProductType(
                operator_info=hafas_rest.OperatorType(
                    name=get_toc_name(request_context, journey_stop.journey.toc.code),
                    id=journey_stop.journey.toc.code,
                ),
                operator_code=journey_stop.journey.toc.code,
                name=journey_stop.journey.headcode,
            )

            if category := journey_stop.journey.map_service_category():
                product.cat_code = category.value
                product.cat_out = category.name()

            departure_board_elements.append((journey_stop.public_departure, hafas_rest.Departure(
                name=journey_stop.journey.headcode,
                type_value=hafas_rest.DepartureType.ST,
                tz=0,
                rt_tz=0,
                stop=get_location_name(request_context, journey_stop.location_id),
                stopid=str(stop_obj.id),
                stop_ext_id=str(journey_stop.location_id),
                lon=decimal.Decimal(stop_obj.longitude),
                lat=decimal.Decimal(stop_obj.latitude),

                date=journey_stop.public_departure.date().isoformat(),
                time=journey_stop.public_departure.time().isoformat(),

                rt_date=rt_departure.date().isoformat() if rt_departure else None,
                rt_time=rt_departure.time().isoformat() if rt_departure else None,

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

                cancelled=journey_stop.journey.cancel_reason is not None,
                part_cancelled=part_cancelled,

                direction=get_location_name(request_context, destination_stop.location_id) if destination_stop else None,
                direction_ext_id=str(destination_stop.location.tiploc) if destination_stop else None,

                date_at_arrival=destination_stop.public_arrival.date().isoformat() if destination_stop else None,
                time_at_arrival=destination_stop.public_arrival.time().isoformat() if destination_stop else None,

                rt_date_at_arrival=destination_arrival.date().isoformat() if destination_arrival else None,
                rt_time_at_arrival=destination_arrival.time().isoformat() if destination_arrival else None,

                uncertain_delay=journey_stop.unknown_delay_departure,

                product=[product],

                stops=hafas_rest.Stops(
                    stop=[darwin_stop_to_hafas(request_context, s) for s in journey_stop.journey.stops.filter(
                        order__gt=journey_stop.order
                    )]
                ),

                journey_detail_ref=hafas_rest.JourneyDetailRef(
                    ref=f"darwin:{journey_stop.journey.rtti_unique_id}"
                ),

                notes=hafas_rest.Notes()
            )))

    departure_board_elements.sort(key=lambda x: x[0])
    departure_board_output = hafas_rest.DepartureBoard(departure=[
        e[1] for e in departure_board_elements
    ])
    return departure_board_output


def darwin_stop_to_hafas(request_context: RequestContext, stop: darwin.models.JourneyStop) -> hafas_rest.StopType:
    monitored_stop = darwin.models.MonitoredStation.objects.filter(crs=stop.location.crs).first()
    own_stop: typing.Optional[tracking.models.Stop] = monitored_stop.linked_stop if monitored_stop else None

    rt_arrival = stop.actual_departure or stop.estimated_departure or None
    rt_departure = stop.actual_departure or stop.estimated_departure or None

    return hafas_rest.StopType(
        id=own_stop.id if own_stop else None,
        name=get_location_name(request_context, stop.location_id),
        ext_id=str(stop.location.tiploc),
        lon=decimal.Decimal(own_stop.longitude) if own_stop else None,
        lat=decimal.Decimal(own_stop.latitude) if own_stop else None,
        dep_tz=0,
        arr_tz=0,
        rt_dep_tz=0,
        rt_arr_tz=0,

        dep_date=stop.public_departure.date().isoformat() if stop.public_departure else None,
        dep_time=stop.public_departure.time().isoformat() if stop.public_departure else None,

        arr_date=stop.public_arrival.date().isoformat() if stop.public_arrival else None,
        arr_time=stop.public_arrival.time().isoformat() if stop.public_arrival else None,

        rt_dep_date=rt_departure.date().isoformat() if rt_departure else None,
        rt_dep_time=rt_departure.time().isoformat() if rt_departure else None,

        rt_arr_date=rt_arrival.date().isoformat() if rt_arrival else None,
        rt_arr_time=rt_arrival.time().isoformat() if rt_arrival else None,

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


def get_location_name(request_context: RequestContext, tiploc: str) -> typing.Optional[str]:
    location = darwin.models.Location.objects.filter(tiploc=tiploc).first()
    if not location:
        return None

    if request_context.language == Language.Welsh and location.crs:
        welsh_name = darwin.models.WelshStationName.objects.filter(crs=location.crs).first()
        if welsh_name:
            return welsh_name.name

    return location.name


def get_toc_name(request_context: RequestContext, toc_code: str) -> typing.Optional[str]:
    toc = darwin.models.TrainOperatingCompany.objects.filter(code=toc_code).first()
    if not toc:
        return None

    if request_context.language == Language.Welsh:
        welsh_name = darwin.models.WelshTrainOperatingCompanyName.objects.filter(toc=toc).first()
        if welsh_name:
            return welsh_name.name

    return toc.name
