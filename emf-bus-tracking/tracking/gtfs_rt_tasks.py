import datetime
import json
import google.protobuf.json_format
from django.db.models import Q
from django.utils import timezone
import emf_bus_tracking.celery
from django.core.files.storage import default_storage
from celery import shared_task
from .gtfs_rt import gtfs_realtime_pb2
from . import models, estimator


@emf_bus_tracking.celery.app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, generate_gtfs_rt.s())


@shared_task(ignore_result=True)
def generate_gtfs_rt():
    now = timezone.now()

    output_message = gtfs_realtime_pb2.FeedMessage(
        header=gtfs_realtime_pb2.FeedHeader(
            gtfs_realtime_version="2.0",
            incrementality=gtfs_realtime_pb2.FeedHeader.FULL_DATASET,
            timestamp=int(now.timestamp()),
        )
    )
    output_message_json = {
        "header": {
            "gtfsRealtimeVersion": "2.0",
            "timestamp": int(now.timestamp()),
        },
        "alerts": [],
        "vehiclePositions": [],
        "tripUpdates": []
    }

    add_alerts(output_message, output_message_json)
    add_vehicle_positions(output_message, output_message_json)
    add_trip_updates(output_message, output_message_json)

    with default_storage.open('gtfs-rt.pb', "wb") as f:
        f.write(output_message.SerializeToString())
    with default_storage.open('gtfs-rt.json', "w") as f:
        json.dump(output_message_json, f, indent=2)


def add_alerts(msg: gtfs_realtime_pb2.FeedMessage, msg_json: dict):
    for alert in models.ServiceAlert.objects.all():
        msg.entity.append(gtfs_realtime_pb2.FeedEntity(
            id=str(alert.id),
            alert=gtfs_realtime_pb2.Alert(
                active_period=map(lambda p: gtfs_realtime_pb2.TimeRange(
                    start=int(p.start.timestamp()) if p.start else None,
                    end=int(p.end.timestamp()) if p.end else None,
                ), alert.periods.all()),
                informed_entity=map(lambda e: gtfs_realtime_pb2.EntitySelector(
                    route_id=str(e.route.id) if e.route else None,
                    trip=gtfs_realtime_pb2.TripDescriptor(
                        trip_id=str(e.journey.id)
                    ) if e.journey else None,
                    stop_id=str(e.stop.id) if e.stop else None,
                ), alert.selectors.all()),
                cause=alert.cause if alert.cause else gtfs_realtime_pb2.Alert.Cause.UNKNOWN_CAUSE,
                effect=alert.effect if alert.effect else gtfs_realtime_pb2.Alert.Effect.UNKNOWN_EFFECT,
                url=gtfs_realtime_pb2.TranslatedString(
                    translation=[gtfs_realtime_pb2.TranslatedString.Translation(
                        text=alert.url,
                    )]
                ) if alert.url else None,
                header_text=gtfs_realtime_pb2.TranslatedString(
                    translation=[gtfs_realtime_pb2.TranslatedString.Translation(
                        text=alert.header,
                    )]
                ) if alert.header else None,
                description_text=gtfs_realtime_pb2.TranslatedString(
                    translation=[gtfs_realtime_pb2.TranslatedString.Translation(
                        text=alert.description,
                    )]
                ) if alert.description else None,
                severity_level=alert.severity if alert.severity else
                gtfs_realtime_pb2.Alert.SeverityLevel.UNKNOWN_SEVERITY,
            )
        ))
        msg_json["alerts"].append({
            "id": str(alert.id),
            "activePeriod": list(map(lambda p: {
                "start": p.start.isoformat() if p.start else None,
                "end": p.end.isoformat() if p.end else None,
            }, alert.periods.all())),
            "informedEntity": list(map(lambda e: {
                "routeId": str(e.route.id) if e.route else None,
                "trip": {
                    "tripId": str(e.journey.id)
                } if e.journey else None,
                "stopId": str(e.stop.id) if e.stop else None,
            }, alert.selectors.all())),
            "cause": alert.get_cause_display() if alert.cause else None,
            "effect": alert.get_effect_display() if alert.effect else None,
            "severityLevel": alert.get_severity_display() if alert.severity else None,
            "url": alert.url if alert.url else None,
            "headerText": alert.header if alert.header else None,
            "descriptionText": alert.description if alert.description else None,
        })


def add_vehicle_positions(msg: gtfs_realtime_pb2.FeedMessage, msg_json: dict):
    cutoff = timezone.now() - estimator.REALTIME_CUTOFF

    for vehicle in models.Vehicle.objects.all():
        last_position = vehicle.positions.order_by('-timestamp').first()
        # if last_position and last_position.timestamp > cutoff:
        if last_position:
            journey = vehicle.journeys.filter(
                real_time_state=models.Journey.RT_STATE_ACTIVE
            ).first()

            current_stop = None
            stop_status = gtfs_realtime_pb2.VehiclePosition.IN_TRANSIT_TO

            if journey:
                current_stop = journey.points.filter(
                    real_time_arrival__isnull=False
                ).order_by('order').last()
                if current_stop:
                    if current_stop.real_time_departure:
                        stop_status = gtfs_realtime_pb2.VehiclePosition.IN_TRANSIT_TO
                    else:
                        stop_status = gtfs_realtime_pb2.VehiclePosition.STOPPED_AT

            vehicle_pb2 = vehicle_descriptor(vehicle)
            trip_pb2 = trip_descriptor(journey) if journey else None

            entity = gtfs_realtime_pb2.FeedEntity(
                id=str(last_position.id),
                vehicle=gtfs_realtime_pb2.VehiclePosition(
                    trip=trip_pb2,
                    vehicle=vehicle_pb2,
                    position=gtfs_realtime_pb2.Position(
                        latitude=last_position.latitude,
                        longitude=last_position.longitude,
                    ),
                    timestamp=int(last_position.timestamp.timestamp()),
                    current_stop_sequence=current_stop.order if current_stop else None,
                    stop_id=str(current_stop.stop.id) if current_stop else None,
                    current_status=stop_status,
                )
            )
            msg.entity.append(entity)
            msg_json["vehiclePositions"].append({
                "id": str(last_position.id),
                "vehicle": google.protobuf.json_format.MessageToDict(vehicle_pb2),
                "trip": google.protobuf.json_format.MessageToDict(trip_pb2) if trip_pb2 else None,
                "position": {
                    "latitude": last_position.latitude,
                    "longitude": last_position.longitude,
                },
                "timestamp": int(last_position.timestamp.timestamp()),
            })


def add_trip_updates(msg: gtfs_realtime_pb2.FeedMessage, msg_json: dict):
    for journey in models.Journey.objects.filter(
        ~Q(real_time_state=models.Journey.RT_STATE_PLANNED)
    ):
        entity = gtfs_realtime_pb2.FeedEntity(
            id=str(journey.id),
            trip_update=gtfs_realtime_pb2.TripUpdate(
                trip=trip_descriptor(journey),
                vehicle=vehicle_descriptor(journey.vehicle) if journey.vehicle else None,
            )
        )

        if journey.vehicle:
            last_position = journey.vehicle.positions.order_by('-timestamp').first()
            if last_position:
                entity.trip_update.timestamp = int(last_position.timestamp.timestamp())

        for point in journey.points.all():
            stop_time_update = gtfs_realtime_pb2.TripUpdate.StopTimeUpdate(
                stop_sequence=point.order,
                stop_id=str(point.stop.id),
            )

            if point.real_time_arrival:
                timestamp = datetime.datetime.combine(journey.date, point.real_time_arrival)
                stop_time_update.arrival.time = int(timestamp.timestamp())
                stop_time_update.arrival.uncertainty = 0
            elif point.estimated_arrival:
                timestamp = datetime.datetime.combine(journey.date, point.estimated_arrival)
                stop_time_update.arrival.time = int(timestamp.timestamp())
            if point.real_time_departure:
                timestamp = datetime.datetime.combine(journey.date, point.real_time_departure)
                stop_time_update.departure.time = int(timestamp.timestamp())
                stop_time_update.departure.uncertainty = 0
            elif point.estimated_departure:
                timestamp = datetime.datetime.combine(journey.date, point.estimated_departure)
                stop_time_update.departure.time = int(timestamp.timestamp())

            if not point.real_time_arrival and not point.real_time_departure \
                    and not point.estimated_arrival and not point.estimated_departure:
                stop_time_update.schedule_relationship = gtfs_realtime_pb2.TripUpdate.StopTimeUpdate.NO_DATA
            else:
                stop_time_update.schedule_relationship = gtfs_realtime_pb2.TripUpdate.StopTimeUpdate.SCHEDULED

            entity.trip_update.stop_time_update.append(stop_time_update)

        msg.entity.append(entity)
        json_entity = google.protobuf.json_format.MessageToDict(entity.trip_update)
        json_entity["id"] = str(journey.id)
        msg_json["tripUpdates"].append(json_entity)


def trip_descriptor(journey: models.Journey):
    return gtfs_realtime_pb2.TripDescriptor(
        trip_id=str(journey.id),
        route_id=str(journey.route.id) if journey.route else None,
        schedule_relationship=gtfs_realtime_pb2.TripDescriptor.CANCELED
        if journey.real_time_state == models.Journey.RT_STATE_CANCELLED else
        gtfs_realtime_pb2.TripDescriptor.SCHEDULED,
    )


def vehicle_descriptor(vehicle: models.Vehicle):
    return gtfs_realtime_pb2.VehicleDescriptor(
        id=str(vehicle.id),
        label=vehicle.name,
        license_plate=vehicle.registration_plate,
    )
