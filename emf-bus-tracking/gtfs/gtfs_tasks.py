import json
import uuid
import zipfile
import csv
import io
import pytz
import docker
from django.utils import timezone
from django.conf import settings
from celery import shared_task
from django.core.files.storage import default_storage
from tracking import models


@shared_task(
    autoretry_for=(Exception,), retry_backoff=1, retry_backoff_max=60, max_retries=10, default_retry_delay=3,
    ignore_result=True
)
def generate_gtfs_schedule():
    now = timezone.now()
    feed_version = f"{now.date().isoformat()}-{uuid.uuid4()}"
    agency_timezone = pytz.timezone(settings.TRANSIT_CONFIG["timezone"])

    output_file = io.BytesIO()
    output_zip = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED, strict_timestamps=False)
    output_json = {
        "routes": []
    }

    with output_zip.open("agency.txt", "w") as file:
        write_agency_file(file, output_json)

    with output_zip.open("stops.txt", "w") as file:
        write_stops_file(file, output_json)

    with output_zip.open("routes.txt", "w") as file:
        write_routes_file(file, output_json)

    with output_zip.open("trips.txt", "w") as file:
        write_trips_file(file, agency_timezone)

    with output_zip.open("stop_times.txt", "w") as file:
        write_stop_times_file(file, agency_timezone)

    with output_zip.open("calendar.txt", "w") as file:
        write_calendar_file(file, agency_timezone)

    with output_zip.open("shapes.txt", "w") as file:
        write_shapes_file(file)

    with output_zip.open("timetables.txt", "w") as file:
        write_timetables_file(file, agency_timezone)

    with output_zip.open("feed_info.txt", "w") as file:
        write_feed_info_file(file, feed_version, output_json)

    output_zip.close()
    with default_storage.open('gtfs.zip', "wb") as f:
        f.write(output_file.getbuffer())
    with default_storage.open('gtfs.json', "w") as f:
        json.dump(output_json, f, indent=True)

    generate_schedule_html.delay()


@shared_task(
    autoretry_for=(Exception,), retry_backoff=1, retry_backoff_max=60, max_retries=10, default_retry_delay=3,
    ignore_result=True
)
def generate_schedule_html():
    client = docker.from_env()

    client.containers.run(settings.GTFS_TO_HTML_DOCKER, auto_remove=True, volumes={
        str(settings.GTFS_TO_HTML_DATA_PATH): {
            "bind": "/data",
            "mode": "rw"
        },
        str(settings.GTFS_TO_HTML_OUTPUT_PATH): {
            "bind": "/html",
            "mode": "rw"
        }
    })


def write_agency_file(file, output_json: dict):
    data = {
        "agency_id": settings.TRANSIT_CONFIG["agency_id"],
        "agency_name": settings.TRANSIT_CONFIG["agency_name"],
        "agency_url": settings.TRANSIT_CONFIG["agency_url"],
        "agency_timezone": settings.TRANSIT_CONFIG["timezone"],
        "agency_lang": settings.GTFS_CONFIG["agency"]["lang"] or "",
        "agency_phone": settings.GTFS_CONFIG["agency"]["phone"] or "",
        "agency_fare_url": settings.GTFS_CONFIG["agency"]["fare_url"] or "",
        "agency_email": settings.GTFS_CONFIG["agency"]["email"] or "",
    }

    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "agency_id",
            "agency_name",
            "agency_url",
            "agency_timezone",
            "agency_lang",
            "agency_phone",
            "agency_fare_url",
            "agency_email",
        ])
        csv_file.writeheader()

        csv_file.writerow(data)

    output_json["agency"] = data


def write_stops_file(file, output_json: dict):
    output_json["stops"] = {}

    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "stop_id",
            "stop_code",
            "stop_name",
            "tts_stop_name",
            "stop_desc",
            "stop_lat",
            "stop_lon",
            "zone_id",
            "stop_url",
            "location_type",
            "parent_station",
            "stop_timezone",
            "wheelchair_boarding",
            "level_id",
            "platform_code",
        ])
        csv_file.writeheader()

        for stop in models.Stop.objects.filter(internal=False):
            data = {
                "stop_id": str(stop.id),
                "stop_code": stop.code or "",
                "stop_name": stop.name,
                "tts_stop_name": "",
                "stop_desc": stop.description or "",
                "stop_lat": stop.latitude,
                "stop_lon": stop.longitude,
                "zone_id": "",
                "stop_url": stop.url or "",
                "location_type": "0",
                "parent_station": "",
                "stop_timezone": "",
                "wheelchair_boarding": "",
                "level_id": "",
                "platform_code": "",
            }
            csv_file.writerow(data)
            output_json["stops"][str(stop.id)] = data


def write_routes_file(file, output_json: dict):
    output_json["routes"] = {}
    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "route_id",
            "agency_id",
            "route_short_name",
            "route_long_name",
            "route_desc",
            "route_type",
            "route_url",
            "route_color",
            "route_text_color",
            "route_sort_order",
            "continuous_pickup",
            "continuous_drop_off",
            "network_id",
        ])
        csv_file.writeheader()

        for route in models.Route.objects.all().order_by('order'):
            data = {
                "route_id": str(route.id),
                "agency_id": settings.TRANSIT_CONFIG["agency_id"],
                "route_short_name": route.name,
                "route_long_name": "",
                "route_desc": route.description or "",
                "route_type": str(route.type),
                "route_url": route.url or "",
                "route_color": route.color[1:] if route.color else "",
                "route_text_color": route.text_color[1:] if route.text_color else "",
                "route_sort_order": str(route.order),
                "continuous_pickup": "",
                "continuous_drop_off": "",
                "network_id": "",
            }
            csv_file.writerow(data)
            output_json["routes"][str(route.id)] = data


def write_trips_file(file, agency_timezone: pytz.timezone):
    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "route_id",
            "service_id",
            "trip_id",
            "trip_headsign",
            "trip_short_name",
            "direction_id",
            "block_id",
            "shape_id",
            "wheelchair_accessible",
            "bikes_allowed"
        ])
        csv_file.writeheader()

        blocks = {}
        forms_from = set()
        for journey in models.Journey.objects.filter(forms_from__isnull=True):
            block_id = uuid.uuid4()
            blocks[journey.id] = block_id
            forms_from.add(journey.id)

        while forms_from:
            new_forms_from = set()
            for journey in models.Journey.objects.filter(forms_from__in=forms_from):
                block_id = blocks[journey.forms_from.id]
                blocks[journey.id] = block_id
                new_forms_from.add(journey.id)
            forms_from = new_forms_from

        for journey in models.Journey.objects.filter(public=True):
            start_date = journey.start_datetime().astimezone(agency_timezone).date()
            csv_file.writerow({
                "route_id": str(journey.route.id),
                "service_id": start_date.isoformat(),
                "trip_id": str(journey.id),
                "trip_headsign": "",
                "trip_short_name": journey.code,
                "direction_id": str(journey.direction),
                "block_id": str(blocks[journey.id]),
                "shape_id": str(journey.shape.id) if journey.shape else "",
                "wheelchair_accessible": "",
                "bikes_allowed": ""
            })


def write_stop_times_file(file, agency_timezone: pytz.timezone):
    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "trip_id",
            "arrival_time",
            "departure_time",
            "stop_id",
            "stop_sequence",
            "stop_headsign",
            "pickup_type",
            "drop_off_type",
            "continuous_pickup",
            "continuous_drop_off",
            "shape_dist_traveled",
            "timepoint",
        ])
        csv_file.writeheader()

        for journey in models.Journey.objects.filter(public=True):
            for stop in journey.points.all():
                arrival_time = stop.arrival_time if stop.arrival_time else stop.departure_time
                departure_time = stop.departure_time if stop.departure_time else stop.arrival_time

                arrival_time = arrival_time.astimezone(agency_timezone)
                departure_time = departure_time.astimezone(agency_timezone)

                csv_file.writerow({
                    "trip_id": str(journey.id),
                    "arrival_time": arrival_time.strftime("%H:%M:%S"),
                    "departure_time": departure_time.strftime("%H:%M:%S"),
                    "stop_id": str(stop.stop.id),
                    "stop_sequence": str(stop.order),
                    "stop_headsign": "",
                    "pickup_type": "",
                    "drop_off_type": "",
                    "continuous_pickup": "",
                    "continuous_drop_off": "",
                    "shape_dist_traveled": "",
                    "timepoint": "1" if stop.journey else "0",
                })


def write_calendar_file(file, agency_timezone: pytz.timezone):
    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "service_id",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "start_date",
            "end_date",
        ])
        csv_file.writeheader()

        seen = set()
        for journey in models.Journey.objects.filter(public=True):
            start_date = journey.start_datetime().astimezone(agency_timezone).date()
            if start_date in seen:
                continue

            seen.add(start_date)
            csv_file.writerow({
                "service_id": start_date.isoformat(),
                "monday": "1" if start_date.weekday() == 0 else "0",
                "tuesday": "1" if start_date.weekday() == 1 else "0",
                "wednesday": "1" if start_date.weekday() == 2 else "0",
                "thursday": "1" if start_date.weekday() == 3 else "0",
                "friday": "1" if start_date.weekday() == 4 else "0",
                "saturday": "1" if start_date.weekday() == 5 else "0",
                "sunday": "1" if start_date.weekday() == 6 else "0",
                "start_date": start_date.strftime("%Y%m%d"),
                "end_date": start_date.strftime("%Y%m%d"),
            })


def write_shapes_file(file):
    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "shape_id",
            "shape_pt_lat",
            "shape_pt_lon",
            "shape_pt_sequence",
            "shape_dist_traveled"
        ])
        csv_file.writeheader()

        for shape in models.ShapePoint.objects.all():
            csv_file.writerow({
                "shape_id": str(shape.shape.id),
                "shape_pt_lat": shape.latitude,
                "shape_pt_lon": shape.longitude,
                "shape_pt_sequence": str(shape.order),
                "shape_dist_traveled": "",
            })


def write_feed_info_file(file, version: str, output_json: dict):
    today = timezone.now().date()
    expiry = today + timezone.timedelta(days=7)

    data = {
        "feed_publisher_name": settings.GTFS_CONFIG["feed"]["publisher"]["name"],
        "feed_publisher_url": settings.GTFS_CONFIG["feed"]["publisher"]["url"],
        "feed_lang": settings.GTFS_CONFIG["feed"]["lang"],
        "default_lang": "",
        "feed_start_date": today.strftime("%Y%m%d"),
        "feed_end_date": expiry.strftime("%Y%m%d"),
        "feed_version": version,
        "feed_contact_email": settings.GTFS_CONFIG["feed"]["contact_email"] or "",
        "feed_contact_url": settings.GTFS_CONFIG["feed"]["contact_url"] or "",
    }

    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "feed_publisher_name",
            "feed_publisher_url",
            "feed_lang",
            "default_lang",
            "feed_start_date",
            "feed_end_date",
            "feed_version",
            "feed_contact_email",
            "feed_contact_url"
        ])
        csv_file.writeheader()

        csv_file.writerow(data)

    output_json["feed_info"] = data


def write_timetables_file(file, agency_timezone: pytz.timezone):
    with io.TextIOWrapper(file, encoding='utf-8', newline='') as text_file:
        csv_file = csv.DictWriter(text_file, fieldnames=[
            "timetable_id",
            "route_id",
            "direction_id",
            "start_date",
            "end_date",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "include_exceptions",
            "timetable_label",
            "service_notes",
            "orientation",
            "direction_name",
            "show_trip_continuation",
        ])
        csv_file.writeheader()

        for route in models.Route.objects.all():
            inbound_dest_point: models.JourneyPoint = models.JourneyPoint.objects.filter(
                journey__route=route,
                journey__direction=models.Journey.DIRECTION_INBOUND
            ).order_by('-order').first()
            outbound_dest_point: models.JourneyPoint = models.JourneyPoint.objects.filter(
                journey__route=route,
                journey__direction=models.Journey.DIRECTION_OUTBOUND
            ).order_by('-order').first()

            start_dates = set()
            for journey in route.journey_set.filter(public=True):
                start_date = journey.start_datetime().astimezone(agency_timezone).date()
                start_dates.add(start_date)

            for date in sorted(start_dates)[::-1]:
                csv_file.writerow({
                    "timetable_id": f"{route.id}-{date.isoformat()}-inbound",
                    "route_id": str(route.id),
                    "direction_id": "0",
                    "start_date": date.strftime("%Y%m%d"),
                    "end_date": date.strftime("%Y%m%d"),
                    "monday": "1" if date.weekday() == 0 else "0",
                    "tuesday": "1" if date.weekday() == 1 else "0",
                    "wednesday": "1" if date.weekday() == 2 else "0",
                    "thursday": "1" if date.weekday() == 3 else "0",
                    "friday": "1" if date.weekday() == 4 else "0",
                    "saturday": "1" if date.weekday() == 5 else "0",
                    "sunday": "1" if date.weekday() == 6 else "0",
                    "include_exceptions": "1",
                    "timetable_label": f"Towards {inbound_dest_point.stop.name} - {date.strftime('%d %b %Y')}",
                    "service_notes": "",
                    "direction_name": "Inbound",
                    "orientation": "horizontal",
                    "show_trip_continuation": "1",
                })
                csv_file.writerow({
                    "timetable_id": f"{route.id}-{date.isoformat()}-outbound",
                    "route_id": str(route.id),
                    "direction_id": "1",
                    "start_date": date.strftime("%Y%m%d"),
                    "end_date": date.strftime("%Y%m%d"),
                    "monday": "1" if date.weekday() == 0 else "0",
                    "tuesday": "1" if date.weekday() == 1 else "0",
                    "wednesday": "1" if date.weekday() == 2 else "0",
                    "thursday": "1" if date.weekday() == 3 else "0",
                    "friday": "1" if date.weekday() == 4 else "0",
                    "saturday": "1" if date.weekday() == 5 else "0",
                    "sunday": "1" if date.weekday() == 6 else "0",
                    "include_exceptions": "1",
                    "timetable_label": f"Towards {outbound_dest_point.stop.name} - {date.strftime('%d %b %Y')}",
                    "service_notes": "",
                    "direction_name": "Outbound",
                    "orientation": "horizontal",
                    "show_trip_continuation": "1",
                })
