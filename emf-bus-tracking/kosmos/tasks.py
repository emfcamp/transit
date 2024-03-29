from celery import shared_task
from . import models, track24_gps, nal_gps
import tracking.models
import tracking.estimator
import base64
import datetime


KNOTS_TO_MS = 0.51444444444444
KMH_TO_MS = 0.27777777777778


@shared_task(
    autoretry_for=(Exception,), retry_backoff=1, retry_backoff_max=60, max_retries=10, default_retry_delay=3,
    ignore_result=True
)
def handle_kosmos_message(message: dict):
    imei = message["header"]["imei"]
    tracker = models.Tracker.objects.filter(imei=imei).first()
    if not tracker:
        return

    if message["type"] == "mo_message":
        if message["payload"] is None:
            return

        payload_bytes = base64.b64decode(message["payload"])

        if tracker.model == tracker.MODEL_TRACK24:
            t24_message = track24_gps.Track24Message.from_bytes(
                payload_bytes, tracker.aes_decryption_key_bytes()
            )

            # GPS position message
            if t24_message.message_type == 0:
                handle_t24_gps(tracker, t24_message, message)
        elif tracker.model == tracker.MODEL_NAL:
            nal_message = nal_gps.NALReport.parse(payload_bytes)
            handle_nal_gps(tracker, nal_message, message)


def handle_t24_gps(tracker: models.Tracker, t24_message: track24_gps.Track24Message, message: dict):
    message_id = message["id"]
    if tracking.models.VehiclePosition.objects.filter(update_id=message_id).count():
        return

    time_of_session = datetime.datetime.fromisoformat(message["header"]["time_of_session"])

    gps_message = track24_gps.GPSData.from_message(t24_message)

    timestamp = datetime.datetime.combine(time_of_session.date(), gps_message.timestamp) \
        .astimezone(datetime.timezone.utc)
    if timestamp > time_of_session:
        timestamp -= datetime.timedelta(days=1)

    if tracker.vehicle:
        last_position = tracker.vehicle.positions.order_by("-timestamp").first()

        tracking.models.VehiclePosition(
            vehicle=tracker.vehicle,
            timestamp=timestamp,
            latitude=gps_message.latitude,
            longitude=gps_message.longitude,
            velocity_ms=gps_message.velocity_knots * KNOTS_TO_MS,
            heading=gps_message.heading,
            update_id=message_id
        ).save()

        if last_position is None or timestamp > last_position.timestamp:
            tracking.estimator.vehicle_report.delay(str(tracker.vehicle.id))


def handle_nal_gps(tracker: models.Tracker, nal_report: nal_gps.NALReport, message: dict):
    message_id = message["id"]
    if tracking.models.VehiclePosition.objects.filter(update_id=message_id).count():
        return

    timestamp = nal_report.time()
    if not timestamp:
        return

    time_of_session = datetime.datetime.fromisoformat(message["header"]["time_of_session"])
    timestamp = datetime.datetime.combine(time_of_session.date(), timestamp) \
        .astimezone(datetime.timezone.utc)
    if timestamp > time_of_session:
        timestamp -= datetime.timedelta(days=1)

    if tracker.vehicle:
        last_position = tracker.vehicle.positions.order_by("-timestamp").first()

        tracking.models.VehiclePosition(
            vehicle=tracker.vehicle,
            timestamp=timestamp,
            latitude=nal_report.latitude(),
            longitude=nal_report.longitude(),
            velocity_ms=nal_report.velocity_ms(),
            heading=nal_report.heading(),
            update_id=message_id
        ).save()

        if last_position is None or timestamp > last_position.timestamp:
            tracking.estimator.vehicle_report.delay(str(tracker.vehicle.id))
