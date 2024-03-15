import shapely
import shapely.ops
import requests
import requests.adapters
import datetime
import typing
import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from . import models, map_lines, consts


LINE_BUFFER = 0.002
LINE_SIMPLIFICATION = 0.0005
FEATURE_LIMIT = 100
OS_SPEED_VALUES = [
    "mf4to7", "mf7to9", "mf9to12", "mf12to14", "mf14to16", "mf16to19", "mf19to22", "mf22to4",
    "ss4to7", "ss7to10", "ss10to14", "ss14to19", "ss19to22", "ss22to4"
]
DAYS_MF = {consts.Days.MONDAY, consts.Days.TUESDAY, consts.Days.WEDNESDAY, consts.Days.THURSDAY, consts.Days.FRIDAY}
DAYS_SS = {consts.Days.SATURDAY, consts.Days.SUNDAY}
DAYS_SM = {consts.Days.SUNDAY, consts.Days.MONDAY}
DAYS_TS = {consts.Days.TUESDAY, consts.Days.WEDNESDAY, consts.Days.THURSDAY, consts.Days.FRIDAY, consts.Days.SATURDAY}


class AverageSpeedException(Exception):
    pass


def get_features_iter(
        s: requests.Session, now: datetime.datetime, filter_polygon: str, offset: int
) -> typing.List[dict]:
    url = 'https://api.os.uk/features/ngd/ofa/v1/collections/trn-rami-averageandindicativespeed-1/items'
    resp = s.get(url, params={
        "key": settings.OS_API_KEY,
        "filter": f"INTERSECTS(geometry, {filter_polygon})",
        "datetime": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "limit": FEATURE_LIMIT,
        "offset": offset,
    })
    resp.raise_for_status()
    return resp.json()["features"]


def get_features(now: datetime.datetime, shape_line: shapely.LineString) -> typing.List[dict]:
    session = requests.Session()
    retries = requests.adapters.Retry(
        total=60, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504, 429],
    )
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))

    path_buffer = shapely.buffer(
        shape_line.simplify(LINE_SIMPLIFICATION), LINE_BUFFER
    ).simplify(LINE_SIMPLIFICATION)

    buffer_points = [f"{p[0]:.5f} {p[1]:.5f}" for p in path_buffer.boundary.coords]
    buffer_polygon = f"POLYGON(({', '.join(buffer_points)}))"

    os_features = []

    offset = 0
    while True:
        try:
            features = get_features_iter(session, now, buffer_polygon, offset)
        except requests.exceptions.RequestException as e:
            raise AverageSpeedException(f"Failed to get features: {e}")

        if not features:
            break

        os_features.extend(features)
        offset += len(features)

    return os_features


def shape_to_line(shape: models.Shape):
    shape_line_points = []
    for point in shape.points.all():
        shape_line_points.append((point.longitude, point.latitude))
    return shapely.LineString(shape_line_points)


def os_features_to_graph(os_data: typing.List[dict], search_path: shapely.LineString):
    graph = map_lines.Graph()

    for feature in os_data:
        if feature["geometry"]["type"] != "LineString":
            continue

        line = shapely.LineString(feature["geometry"]["coordinates"])

        in_direction_speeds = [f"averagespeed_{f}indirection_kph" for f in OS_SPEED_VALUES]
        out_direction_speeds = [f"averagespeed_{f}againstdirection_kph" for f in OS_SPEED_VALUES]

        in_direction = all(feature["properties"][k] for k in in_direction_speeds)
        out_direction = all(feature["properties"][k] for k in out_direction_speeds)

        last_point = None
        for point in line.coords:
            point = shapely.geometry.Point(point)
            if last_point:
                graph.add_edge(
                    a=last_point, b=point,
                    length=float(point.distance(search_path)),
                    data=map_lines.EdgeProperties(
                        id=feature["id"],
                        data=feature["properties"]
                    ),
                    forward_direction=in_direction,
                    backward_direction=out_direction
                )
            last_point = point

    return graph


def add_average_speed(
        point: models.ShapePoint, days: typing.Set[consts.Days], start: datetime.time, end: datetime.time, speed: float,
        direction: int
):
    new_speed = models.ShapePointAverageSpeed()
    new_speed.point = point
    new_speed.speed_kmh = speed
    new_speed.validity_start_time = start
    new_speed.validity_end_time = end
    new_speed.valid_monday = consts.Days.MONDAY in days
    new_speed.valid_tuesday = consts.Days.TUESDAY in days
    new_speed.valid_wednesday = consts.Days.WEDNESDAY in days
    new_speed.valid_thursday = consts.Days.THURSDAY in days
    new_speed.valid_friday = consts.Days.FRIDAY in days
    new_speed.valid_saturday = consts.Days.SATURDAY in days
    new_speed.valid_sunday = consts.Days.SUNDAY in days
    new_speed.direction = direction
    new_speed.save()


@shared_task
def update_average_speed_data(shape_id):
    shape = models.Shape.objects.get(id=shape_id)
    now = timezone.now()

    try:
        shape_line = shape_to_line(shape)

        logging.info("Getting features from OS")
        os_features = get_features(now, shape_line)

        logging.info("Converting features to graph")
        graph = os_features_to_graph(os_features, shape_line)

        logging.info("Finding largest connected component in graph")
        graph = graph.largest_connected_component()

        logging.info("Finding matching path through graph")
        graph_path = map_lines.find_matching_graph_path(graph, shape_line)
        if graph_path is None:
            raise AverageSpeedException("No matching path found")

        logging.info("Mapping path properties to original line")
        line_parts = map_lines.map_properties(graph_path, shape_line)

        logging.info("Updating database")
        with transaction.atomic():
            shape.last_average_speed_update = now
            shape.save()
            shape.points.all().delete()

            order = 0

            for part in line_parts:
                direction = "indirection" if part.direction == map_lines.EdgeDirection.FORWARD else "againstdirection"
                reverse_direction = \
                    "indirection" if part.direction == map_lines.EdgeDirection.BACKWARD else "againstdirection"

                speed_limit = part.data["indicativespeedlimit_kph"]
                speed_mf_4_7 = part.data[f"averagespeed_mf4to7{direction}_kph"]
                reverse_speed_mf_4_7 = part.data[f"averagespeed_mf4to7{reverse_direction}_kph"] or speed_mf_4_7
                speed_mf_7_9 = part.data[f"averagespeed_mf7to9{direction}_kph"]
                reverse_speed_mf_7_9 = part.data[f"averagespeed_mf7to9{reverse_direction}_kph"] or speed_mf_7_9
                speed_mf_9_12 = part.data[f"averagespeed_mf9to12{direction}_kph"]
                reverse_speed_mf_9_12 = part.data[f"averagespeed_mf9to12{reverse_direction}_kph"] or speed_mf_9_12
                speed_mf_12_14 = part.data[f"averagespeed_mf12to14{direction}_kph"]
                reverse_speed_mf_12_14 = part.data[f"averagespeed_mf12to14{reverse_direction}_kph"] or speed_mf_12_14
                speed_mf_14_16 = part.data[f"averagespeed_mf14to16{direction}_kph"]
                reverse_speed_mf_14_16 = part.data[f"averagespeed_mf14to16{reverse_direction}_kph"] or speed_mf_14_16
                speed_mf_16_19 = part.data[f"averagespeed_mf16to19{direction}_kph"]
                reverse_speed_mf_16_19 = part.data[f"averagespeed_mf16to19{reverse_direction}_kph"] or speed_mf_16_19
                speed_mf_19_22 = part.data[f"averagespeed_mf19to22{direction}_kph"]
                reverse_speed_mf_19_22 = part.data[f"averagespeed_mf19to22{reverse_direction}_kph"] or speed_mf_19_22
                speed_mf_22_4 = part.data[f"averagespeed_mf22to4{direction}_kph"]
                reverse_speed_mf_22_4 = part.data[f"averagespeed_mf22to4{reverse_direction}_kph"] or speed_mf_22_4
                speed_ss_4_7 = part.data[f"averagespeed_ss4to7{direction}_kph"]
                reverse_speed_ss_4_7 = part.data[f"averagespeed_ss4to7{reverse_direction}_kph"] or speed_ss_4_7
                speed_ss_7_10 = part.data[f"averagespeed_ss7to10{direction}_kph"]
                reverse_speed_ss_7_10 = part.data[f"averagespeed_ss7to10{reverse_direction}_kph"] or speed_ss_7_10
                speed_ss_10_14 = part.data[f"averagespeed_ss10to14{direction}_kph"]
                reverse_speed_ss_10_14 = part.data[f"averagespeed_ss10to14{reverse_direction}_kph"] or speed_ss_10_14
                speed_ss_14_19 = part.data[f"averagespeed_ss14to19{direction}_kph"]
                reverse_speed_ss_14_19 = part.data[f"averagespeed_ss14to19{reverse_direction}_kph"] or speed_ss_14_19
                speed_ss_19_22 = part.data[f"averagespeed_ss19to22{direction}_kph"]
                reverse_speed_ss_19_22 = part.data[f"averagespeed_ss19to22{reverse_direction}_kph"] or speed_ss_19_22
                speed_ss_22_4 = part.data[f"averagespeed_ss22to4{direction}_kph"]
                reverse_speed_ss_22_4 = part.data[f"averagespeed_ss22to4{reverse_direction}_kph"] or speed_ss_22_4

                for point in part.line.coords[:-1]:
                    order += 1
                    new_point = models.ShapePoint()
                    new_point.shape = shape
                    new_point.longitude = point[0]
                    new_point.latitude = point[1]
                    new_point.order = order
                    new_point.speed_limit_kmh = speed_limit
                    new_point.save()

                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(4, 0), datetime.time(6, 59, 59, 999999),
                        speed_mf_4_7, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(4, 0), datetime.time(6, 59, 59, 999999),
                        reverse_speed_mf_4_7, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(7, 0), datetime.time(8, 59, 59, 999999),
                        speed_mf_7_9, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(7, 0), datetime.time(8, 59, 59, 999999),
                        reverse_speed_mf_7_9, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(9, 0), datetime.time(11, 59, 59, 999999),
                        speed_mf_9_12, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(9, 0), datetime.time(11, 59, 59, 999999),
                        reverse_speed_mf_9_12, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(12, 0), datetime.time(13, 59, 59, 999999),
                        speed_mf_12_14, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(12, 0), datetime.time(13, 59, 59, 999999),
                        reverse_speed_mf_12_14, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(14, 0), datetime.time(15, 59, 59, 999999),
                        speed_mf_14_16, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(14, 0), datetime.time(15, 59, 59, 999999),
                        reverse_speed_mf_14_16, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(16, 0), datetime.time(18, 59, 59, 999999),
                        speed_mf_16_19, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(16, 0), datetime.time(18, 59, 59, 999999),
                        reverse_speed_mf_16_19, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(19, 0), datetime.time(23, 59, 59, 999999),
                        speed_mf_19_22, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(19, 0), datetime.time(23, 59, 59, 999999),
                        reverse_speed_mf_19_22, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(22, 0), datetime.time(23, 59, 59, 999999),
                        speed_mf_22_4, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_MF,
                        datetime.time(22, 0), datetime.time(23, 59, 59, 999999),
                        reverse_speed_mf_22_4, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_TS,
                        datetime.time(0, 0), datetime.time(3, 59, 59, 999999),
                        speed_mf_22_4, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_TS,
                        datetime.time(0, 0), datetime.time(3, 59, 59, 999999),
                        reverse_speed_mf_22_4, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(4, 0), datetime.time(6, 59, 59, 999999),
                        speed_ss_4_7, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(4, 0), datetime.time(6, 59, 59, 999999),
                        reverse_speed_ss_4_7, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(7, 0), datetime.time(9, 59, 59, 999999),
                        speed_ss_7_10, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(7, 0), datetime.time(9, 59, 59, 999999),
                        reverse_speed_ss_7_10, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(10, 0), datetime.time(13, 59, 59, 999999),
                        speed_ss_10_14, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(10, 0), datetime.time(13, 59, 59, 999999),
                        reverse_speed_ss_10_14, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(14, 0), datetime.time(19, 59, 59, 999999),
                        speed_ss_14_19, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(14, 0), datetime.time(19, 59, 59, 999999),
                        reverse_speed_ss_14_19, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(19, 0), datetime.time(21, 59, 59, 999999),
                        speed_ss_19_22, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(19, 0), datetime.time(21, 59, 59, 999999),
                        reverse_speed_ss_19_22, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(22, 0), datetime.time(23, 59, 59, 999999),
                        speed_ss_22_4, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_SS,
                        datetime.time(22, 0), datetime.time(23, 59, 59, 999999),
                        reverse_speed_ss_22_4, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )
                    add_average_speed(
                        new_point, DAYS_SM,
                        datetime.time(0, 0), datetime.time(3, 59, 59, 999999),
                        speed_ss_22_4, models.ShapePointAverageSpeed.DIRECTION_FORWARD
                    )
                    add_average_speed(
                        new_point, DAYS_SM,
                        datetime.time(0, 0), datetime.time(3, 59, 59, 999999),
                        reverse_speed_ss_22_4, models.ShapePointAverageSpeed.DIRECTION_REVERSE
                    )

    except AverageSpeedException as e:
        return str(e)

    return None
