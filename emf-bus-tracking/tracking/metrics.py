import prometheus_client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models


@csrf_exempt
def metrics(_request):
    registry = prometheus_client.CollectorRegistry()
    vehicle_speed = prometheus_client.Gauge(
        'tfemf_vehicle_speed_ms', 'The last known speed of a vehicle',
        labelnames=['vehicle'],
        registry=registry
    )
    vehicle_lat = prometheus_client.Gauge(
        'tfemf_vehicle_lat', 'The last known latitude of a vehicle',
        labelnames=['vehicle'],
        registry=registry
    )
    vehicle_long = prometheus_client.Gauge(
        'tfemf_vehicle_long', 'The last known longitude of a vehicle',
        labelnames=['vehicle'],
        registry=registry
    )
    vehicle_heading = prometheus_client.Gauge(
        'tfemf_vehicle_heading', 'The last known heading of a vehicle',
        labelnames=['vehicle'],
        registry=registry
    )
    vehicle_timestamp = prometheus_client.Gauge(
        'tfemf_vehicle_last_update_timestamp', 'The time of the last position update of a vehicle',
        labelnames=['vehicle'],
        registry=registry
    )

    for vehicle in models.Vehicle.objects.all():
        last_position = vehicle.positions.order_by("-timestamp").first()
        if last_position:
            vehicle_timestamp.labels(vehicle=str(vehicle.id)).set(int(last_position.timestamp.timestamp()))
            vehicle_lat.labels(vehicle=str(vehicle.id)).set(last_position.latitude)
            vehicle_long.labels(vehicle=str(vehicle.id)).set(last_position.longitude)
            if last_position.velocity_ms:
                vehicle_speed.labels(vehicle=str(vehicle.id)).set(last_position.velocity_ms)
            if last_position.heading:
                vehicle_heading.labels(vehicle=str(vehicle.id)).set(last_position.heading)

    output = prometheus_client.generate_latest(registry)
    return HttpResponse(output, content_type="text/plain")
