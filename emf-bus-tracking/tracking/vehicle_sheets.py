import base64
import datetime
import json
import polyline
import pytz
import urllib.parse
import cryptography.hazmat.primitives.asymmetric.ec
import cryptography.hazmat.primitives.hashes
from . import models
from django.conf import settings
from django.db.models import Min
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404


def make_mapkit_url(params: dict) -> str:
    params["teamId"] = settings.APPLE_MAPS_TEAM_ID
    params["keyId"] = settings.APPLE_MAPS_KEY_ID
    url_params = urllib.parse.urlencode(params)
    tbs_url = f"/api/v1/snapshot?{url_params}"
    signature = settings.APPLE_MAPS_KEY.sign(
        tbs_url.encode(),
        cryptography.hazmat.primitives.asymmetric.ec.ECDSA(
            cryptography.hazmat.primitives.hashes.SHA256()
        )
    )
    signature_str = base64.urlsafe_b64encode(signature).decode()
    return f"https://snapshot.apple-mapkit.com{tbs_url}&signature={signature_str}"


def make_shape(shape: models.Shape) -> dict:
    points = list(shape.points.order_by("order").values("latitude", "longitude"))
    map_url = make_mapkit_url({
        "center": "auto",
        "poi": 0,
        "lang": "en-GB",
        "size": "600x300",
        "t": "standard",
        "colorScheme": "light",
        "scale": 2,
        "overlays": json.dumps([{
            "type": "polyline",
            "points": polyline.encode([(point["latitude"], point["longitude"]) for point in points]),
            "strokeColor": "ff0000",
            "lineWidth": 5,
            "strokeOpacity": 0.5
        }])
    })

    return {
        "name": shape.name,
        "url": map_url
    }


@permission_required("tracking.view_vehicle")
@permission_required("tracking.view_journey")
@permission_required("tracking.view_journeypoint")
def vehicle_sheet(request, vehicle_id, service_date: datetime.date):
    vehicle_obj = get_object_or_404(models.Vehicle, id=vehicle_id)

    timezone = pytz.timezone(settings.TRANSIT_CONFIG["timezone"])

    block_starts = models.Journey.objects.filter(
        vehicle=vehicle_obj, forms_from__isnull=True
    ).annotate(
        start_time=Min("points__departure_time")
    ).filter(
        start_time__date=service_date
    )

    blocks = []
    shapes = {}

    for block_start in block_starts:
        block = []
        next_journey = block_start
        last_time = None
        while next_journey:
            first_point = next_journey.points.order_by("order").first()
            first_time = first_point.arrival_time if first_point.arrival_time else first_point.departure_time

            wait_time = first_time - last_time if last_time else None
            if wait_time:
                block.append({
                    "type": "wait",
                    "hours": wait_time.seconds // 3600,
                    "minutes": (wait_time.seconds // 60) % 60,
                })

            block.append({
                "type": "new_journey",
                "code": next_journey.code,
                "route": {
                    "name": next_journey.route.name,
                    "colour": next_journey.route.color,
                    "text_colour": next_journey.route.text_color,
                } if next_journey.route else None,
                "direction": next_journey.get_direction_display(),
                "public": next_journey.public,
                "shape": next_journey.shape.name if next_journey.shape else None,
            })

            if next_journey.shape_id and next_journey.shape_id not in shapes:
                shapes[next_journey.shape_id] = make_shape(next_journey.shape)

            for point in next_journey.points.order_by("order"):
                if point.arrival_time:
                    block.append({
                        "type": "point_arrival",
                        "name": point.stop.internal_name,
                        "time": point.arrival_time.astimezone(timezone).replace(tzinfo=None),
                    })
                    last_time = point.arrival_time

                if point.departure_time:
                    block.append({
                        "type": "point_departure",
                        "name": point.stop.internal_name,
                        "time": point.departure_time.astimezone(timezone).replace(tzinfo=None),
                    })
                    last_time = point.departure_time

            next_journey = next_journey.forms_into_opt()

        blocks.append(block)

    return render(request, "tracking/vehicle_sheet.html", {
        "vehicle": vehicle_obj,
        "service_date": service_date,
        "blocks": blocks,
        "shapes": shapes.values(),
    })
