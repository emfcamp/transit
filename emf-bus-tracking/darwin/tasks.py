import datetime
import logging
import typing

import boto3
import re
import gzip
import xsdata.formats.dataclass.parsers
from celery import shared_task
from django.conf import settings
from django.db.models import Q
from django.db import transaction
from django.core.cache import cache
from . import push_port, models

TT_BUCKET = "darwin.xmltimetable"
FILE_PREFIX = "PPTimetable/"
TT_RE = re.compile(r"^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(\d{6})_v8.xml.gz$")
TT_REF_RE = re.compile(r"^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(\d{6})_ref_v3.xml.gz$")


dict_decoder = xsdata.formats.dataclass.parsers.DictDecoder()
xml_parser = xsdata.formats.dataclass.parsers.XmlParser()


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.DARWIN_S3_ACCESS_KEY,
        aws_secret_access_key=settings.DARWIN_S3_SECRET_KEY,
        region_name="eu-west-1",
    )


def get_tiploc_filter() -> typing.Set[str]:
    if tiploc_filter := cache.get("darwin_tiploc_filter"):
        return tiploc_filter

    tiploc_filter = set()
    for loc in models.MonitoredStation.objects.all():
        if location := loc.location():
            tiploc_filter.add(location.tiploc)

    cache.set("darwin_tiploc_filter", tiploc_filter, 60)

    return tiploc_filter


def get_rid_filter() -> typing.Set[str]:
    if rid_filter := cache.get("darwin_rid_filter"):
        return rid_filter

    rid_filter = set()
    for journey in models.Journey.objects.all():
        rid_filter.add(journey.rtti_unique_id)

    cache.set("darwin_rid_filter", rid_filter, 60)

    return rid_filter


@shared_task(
    autoretry_for=(Exception,), retry_backoff=1, retry_backoff_max=60, max_retries=100, default_retry_delay=3,
    ignore_result=True
)
def process_darwin_message(
        sequence_number: int,
        message_type: str,
        timestamp: float,
        message: dict
):
    timestamp = datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
    message: push_port.rtti_pptschema_v16.Pport = dict_decoder.decode(message, push_port.rtti_pptschema_v16.Pport)

    if message.time_table_id:
        tt_file = message.time_table_id.ttfile.strip()
        tt_ref_file = message.time_table_id.ttreffile.strip()

        if tt_file:
            logging.info(f"{timestamp} - new timetable file: {tt_file}")
            if TT_RE.match(tt_file):
                download_tt_file.delay(tt_file)
        if tt_ref_file:
            logging.info(f"{timestamp} - new timetable reference file: {tt_ref_file}")
            if TT_REF_RE.match(tt_ref_file):
                download_tt_ref_file.delay(tt_ref_file)

    if message.s_r:
        handle_data_response(message.s_r, timestamp)

    if message.u_r:
        handle_data_response(message.u_r, timestamp)


def handle_data_response(data: push_port.rtti_pptschema_v16.DataResponse, timestamp: datetime.datetime):
    tiploc_filter = get_tiploc_filter()
    rid_filter = get_rid_filter()

    for schedule in data.schedule:
        rid = handle_journey(schedule, tiploc_filter)
        if rid:
            logging.info(f"{timestamp} - new schedule: {rid}")
            cache.delete("darwin_rid_filter")

    for station_message in data.ow:
        handle_station_message(station_message, timestamp)

    for deactivated_schedule in data.deactivated:
        handle_deactivated_journey(deactivated_schedule, rid_filter, timestamp)

    for train_status in data.ts:
        handle_train_status(train_status, rid_filter, timestamp)


def handle_journey(
        journey: typing.Union[push_port.rtti_cttschema_v8.PportTimetable, push_port.rtti_pptschedules_v3.Schedule],
        tiploc_filter: typing.Set[str],
) -> typing.Optional[str]:
    if not journey.is_passenger_svc or journey.deleted:
        return

    calling_tiplocs = set()
    for op in journey.or_value:
        calling_tiplocs.add(op.tpl)
    for ip in journey.ip:
        calling_tiplocs.add(ip.tpl)
    for dp in journey.dt:
        calling_tiplocs.add(dp.tpl)

    if not calling_tiplocs & tiploc_filter:
        return

    ssd = datetime.date(
        year=journey.ssd.year,
        month=journey.ssd.month,
        day=journey.ssd.day,
    )

    with transaction.atomic():
        journey_obj, _ = models.Journey.objects.update_or_create(
            rtti_unique_id=journey.rid,
            defaults={
                "date": ssd,
                "cancel_reason_id": journey.cancel_reason.value if journey.cancel_reason else None,
                "cancel_location_id": journey.cancel_reason.tiploc if journey.cancel_reason else None,
                "cancel_reason_near": journey.cancel_reason.near if journey.cancel_reason else False,
                "uid": journey.uid,
                "headcode": journey.train_id,
                "toc_id": journey.toc,
                "activated": journey.is_active if hasattr(journey, 'is_active') else (not getattr(journey, 'qtrain', False)),
            }
        )
        journey_obj.stops.all().delete()

        order = 1
        for op in journey.or_value:
            models.JourneyStop.objects.create(
                journey=journey_obj,
                location_id=op.tpl,
                order=order,
                canceled=op.can,
                planned_platform=getattr(op, 'plat', None),
                public_arrival=op.pta,
                public_departure=op.ptd,
                working_arrival=op.wta,
                working_departure=op.wtd,
                use_false_destination=op.fd or False,
                origin=True,
                destination=False,
            )
            order += 1

        for ip in journey.ip:
            models.JourneyStop.objects.create(
                journey=journey_obj,
                location_id=ip.tpl,
                order=order,
                canceled=ip.can,
                planned_platform=getattr(ip, 'plat', None),
                public_arrival=ip.pta,
                public_departure=ip.ptd,
                working_arrival=ip.wta,
                working_departure=ip.wtd,
                use_false_destination=ip.fd or False,
                origin=False,
                destination=False,
            )
            order += 1

        for dp in journey.dt:
            models.JourneyStop.objects.create(
                journey=journey_obj,
                location_id=dp.tpl,
                order=order,
                canceled=dp.can,
                planned_platform=getattr(dp, 'plat', None),
                public_arrival=dp.pta,
                public_departure=dp.ptd,
                working_arrival=dp.wta,
                working_departure=dp.wtd,
                use_false_destination=False,
                origin=False,
                destination=True,
            )
            order += 1

    return journey.rid


def handle_deactivated_journey(
        journey: push_port.rtti_pptschedules_v2.DeactivatedSchedule,
        rid_filter: typing.Set[str],
        timestamp: datetime.datetime
):
    if journey.rid not in rid_filter:
        return

    journey_obj: models.Journey = models.Journey.objects.filter(rtti_unique_id=journey.rid).first()
    if not journey_obj:
        return

    logging.info(f"{timestamp} - deactivated schedule: {journey.rid}")
    journey_obj.activated = False
    journey_obj.save()


def handle_station_message(message: push_port.rtti_pptstation_messages_v1.StationMessage, timestamp: datetime.datetime):
    monitored_crs = set(models.MonitoredStation.objects.values_list("crs", flat=True))

    monitored = False
    for station in message.station:
        if station.crs in monitored_crs:
            monitored = True
            break

    if not monitored:
        models.Message.objects.filter(message_id=message.id).delete()
        return

    logging.info(f"{timestamp} - new station message: {message.id}")

    with transaction.atomic():
        message_obj, _ = models.Message.objects.update_or_create(
            message_id=message.id,
            defaults={
                "message": str(message.msg),
                "category": message.cat.value,
                "severity": message.sev.value,
                "supress_rtt": message.suppress,
            }
        )
        message_obj.stations.all().delete()

        for station in message.station:
            models.MessageStation.objects.create(
                message=message_obj,
                crs=station.crs,
            )


def handle_train_status(
        status: push_port.rtti_pptforecasts_v3.Ts,
        rid_filter: typing.Set[str],
        timestamp: datetime.datetime
):
    if status.rid not in rid_filter:
        return

    journey_obj: models.Journey = models.Journey.objects.filter(rtti_unique_id=status.rid).first()
    if not journey_obj:
        return

    logging.info(f"{timestamp} - train status: {status.rid}")

    with transaction.atomic():
        journey_obj.late_reason_id = status.late_reason.value if status.late_reason else None
        journey_obj.late_reason_location_id = status.late_reason.tiploc if status.late_reason else None
        journey_obj.late_reason_near = status.late_reason.near if status.late_reason else False
        journey_obj.save()

        for location in status.location:
            journey_stop: models.JourneyStop = journey_obj.stops.filter(location_id=location.tpl).first()
            if not journey_stop:
                continue

            journey_stop.supress = location.suppr or False

            if location.plat:
                journey_stop.current_platform = location.plat.value
                journey_stop.platform_suppressed = location.plat.platsup
                journey_stop.platform_confirmed = location.plat.conf

            if location.arr:
                if location.arr.at:
                    journey_stop.actual_arrival = datetime.datetime.strptime(location.arr.at, "%H:%M").time()
                if location.arr.at_removed:
                    journey_stop.actual_arrival = None
                if location.arr.et:
                    journey_stop.estimated_arrival = datetime.datetime.strptime(location.arr.et, "%H:%M").time()
                journey_stop.unknown_delay_arrival = location.arr.delayed or False
            if location.dep:
                if location.dep.at:
                    journey_stop.actual_departure = datetime.datetime.strptime(location.dep.at, "%H:%M").time()
                if location.dep.at_removed:
                    journey_stop.actual_departure = None
                if location.dep.et:
                    journey_stop.estimated_departure = datetime.datetime.strptime(location.dep.et, "%H:%M").time()
                journey_stop.unknown_delay_departure = location.dep.delayed or False

            journey_stop.save()


@shared_task(
    autoretry_for=(Exception,), retry_backoff=1, retry_backoff_max=60, max_retries=100, default_retry_delay=3,
    ignore_result=True
)
def download_tt_file(name: str):
    logging.info(f"Downloading timetable file {name}")
    tt: push_port.PportTimetable = get_tt_file(name, push_port.PportTimetable)

    tiploc_filter = get_tiploc_filter()
    seen_rtti_unique_ids = set()

    for journey in tt.journey:
        rid = handle_journey(journey, tiploc_filter)
        if rid:
            seen_rtti_unique_ids.add(rid)

    models.Journey.objects.filter(~Q(rtti_unique_id__in=seen_rtti_unique_ids)).delete()
    cache.delete("darwin_rid_filter")


@shared_task(
    autoretry_for=(Exception,), retry_backoff=1, retry_backoff_max=60, max_retries=100, default_retry_delay=3,
    ignore_result=True
)
def download_tt_ref_file(name: str):
    logging.info(f"Downloading timetable reference file {name}")
    tt_ref: push_port.PportTimetableRef = get_tt_file(name, push_port.PportTimetableRef)

    with transaction.atomic():
        models.TrainOperatingCompany.objects.all().delete()
        for toc in tt_ref.toc_ref:
            models.TrainOperatingCompany.objects.create(
                code=toc.toc,
                name=toc.tocname,
                website=toc.url,
            )

        models.Location.objects.all().delete()
        for location in tt_ref.location_ref:
            models.Location.objects.create(
                tiploc=location.tpl,
                crs=location.crs,
                toc_id=location.toc,
                name=location.locname,
            )

        models.LateRunningReason.objects.all().delete()
        for reason in tt_ref.late_running_reasons.reason:
            models.LateRunningReason.objects.create(
                code=reason.code,
                description=reason.reasontext,
            )

        models.CancellationReason.objects.all().delete()
        for reason in tt_ref.cancellation_reasons.reason:
            models.CancellationReason.objects.create(
                code=reason.code,
                description=reason.reasontext,
            )


def get_tt_file(name: str, data_type):
    s3_client = get_s3_client()
    s3_object = s3_client.get_object(Bucket=TT_BUCKET, Key=f"{FILE_PREFIX}{name}")

    tt_str = gzip.open(s3_object["Body"]).read().decode("utf-8")
    tt = xml_parser.from_string(tt_str, data_type)

    return tt
