import enum
import json
import secrets
import dataclasses
import traceback
import datetime
import xsdata.formats.dataclass.serializers.xml
import xsdata.formats.dataclass.serializers.json
from django.http import HttpResponse
from django.utils import timezone
import tracking.models
from . import hafas_rest


class DataFormat(enum.Enum):
    XML = "xml"
    JSON = "json"


@dataclasses.dataclass
class RequestContext:
    data_format: DataFormat
    request_id: str
    request_data: dict
    request_time: datetime.datetime


def encode_json(obj):
    if not dataclasses.is_dataclass(obj):
        return {"value": obj}

    out = {}
    fields = dataclasses.fields(obj)

    for field in fields:
        value = getattr(obj, field.name)
        if value:
            field_type = field.metadata.get("type", None)
            field_name = field.metadata.get("name", field.name)
            if field_type == "Element":
                if isinstance(value, list):
                    out[field_name] = [encode_json(v) for v in value]
                else:
                    out[field_name] = encode_json(value)
            elif field_type == "Attribute":
                out[field_name] = value

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
    now = timezone.now()

    stop_id = request_context.request_data.get("id", None)
    if not stop_id:
        return hafas_rest.CommonResponseType(
            error_code="400",
            error_text="Missing id",
        )
    stop_obj = tracking.models.Stop.objects.filter(id=stop_id).first()
    if not stop_obj:
        return hafas_rest.CommonResponseType(
            error_code="404",
            error_text=f"Stop not found: {stop_id}",
        )

    date = request_context.request_data.get("date", None)
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

    time = request_context.request_data.get("time", None)
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
    if duration := request_context.request_data.get("duration", None):
        try:
            search_minutes = max(int(duration), 1439)
        except ValueError:
            return hafas_rest.CommonResponseType(
                error_code="400",
                error_text=f"Invalid duration: {duration}",
            )

    search_lines = []
    if lines := request_context.request_data.get("lines", None):
        for line_id in lines.split(","):
            negative_search = False
            if line_id.startswith("!"):
                negative_search = True
            line = tracking.models.Route.objects.filter(id=line_id).first()
            if not line:
                return hafas_rest.CommonResponseType(
                    error_code="404",
                    error_text=f"Line not found: {line_id}",
                )
            search_lines.append((line, negative_search))
