import dataclasses
import enum
import typing
import datetime
import scipy.spatial
import shapely
import geographiclib.geodesic
import logging
import contextlib
import time
import django.core.cache
import emf_bus_tracking.celery
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from . import models, consts

WGS84_GEOD = geographiclib.geodesic.Geodesic(6378.137, 1 / 298.257223563)  # major, flattening
REALTIME_CUTOFF = datetime.timedelta(minutes=15)
STOP_SEARCH_RADIUS_METERS = 75
MINIMUM_STOP_TIME = datetime.timedelta(seconds=60)
GPS_VARIANCE = 2.5

LOCK_EXPIRE = 60 * 5  # 5 minutes


@emf_bus_tracking.celery.app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15.0, update_journey_estimates.s())


@contextlib.contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    status = django.core.cache.cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            django.core.cache.cache.delete(lock_id)


@dataclasses.dataclass
class SpeedAtTime:
    from_time: datetime.time
    to_time: datetime.time
    speed_ms: float


@dataclasses.dataclass
class Speed:
    monday: typing.List[SpeedAtTime]
    tuesday: typing.List[SpeedAtTime]
    wednesday: typing.List[SpeedAtTime]
    thursday: typing.List[SpeedAtTime]
    friday: typing.List[SpeedAtTime]
    saturday: typing.List[SpeedAtTime]
    sunday: typing.List[SpeedAtTime]
    limit_ms: float

    def average_speed_at_time(self, time: datetime.datetime):
        day = time.weekday()
        speed_map = {
            0: self.monday,
            1: self.tuesday,
            2: self.wednesday,
            3: self.thursday,
            4: self.friday,
            5: self.saturday,
            6: self.sunday
        }

        for speed in speed_map[day]:
            if speed.from_time <= time.time() <= speed.to_time:
                return speed.speed_ms

        return self.limit_ms


class Point:
    point: shapely.Point

    def __init__(self, lat: float, long: float):
        self.point = shapely.Point(long, lat)

    def __str__(self):
        return str(self.point)

    def distance_to(self, other: "Point") -> float:
        return WGS84_GEOD.Inverse(
            self.lat, self.long, other.lat, other.long,
            geographiclib.geodesic.Geodesic.DISTANCE
        )["s12"] * 1000  # km to m

    @property
    def lat(self) -> float:
        return self.point.y

    @property
    def long(self) -> float:
        return self.point.x

    @property
    def x(self) -> float:
        return self.point.x

    @property
    def y(self) -> float:
        return self.point.y


class Path:
    stops: typing.List[Point]
    distances: typing.List[float]
    speeds: typing.List[Speed]
    kd_tree: scipy.spatial.KDTree

    def __init__(self, points: typing.List[Point], speeds: typing.List[Speed]):
        self.points = points
        self.distances = []
        self.speeds = speeds
        self.kd_tree = scipy.spatial.KDTree([(p.x, p.y) for p in points])

    def calculate_distances(self):
        for i, point in enumerate(self.points[:-1]):
            next_point = self.points[i + 1]

            dist = point.distance_to(next_point)
            self.distances.append(dist)

    def point(self, i: int) -> Point:
        return self.points[i]

    def get_closest_points(self, point: Point, k: int) -> typing.List[typing.Tuple[Point, int]]:
        _, idx = self.kd_tree.query((point.x, point.y), k=k)
        return [(self.points[i], i) for i in idx] if k > 1 else [(self.points[idx], idx)]

    def distance_between(self, i: int, j: int) -> float:
        return sum(self.distances[i:j])

    def distance_to_end(self, i: int) -> float:
        return sum(self.distances[i:])


def map_point_speed(average_speeds: typing.List[models.ShapePointAverageSpeed]) -> typing.List[SpeedAtTime]:
    speed_map = []
    for speed in average_speeds:
        speed_map.append(SpeedAtTime(
            from_time=speed.validity_start_time,
            to_time=speed.validity_end_time,
            speed_ms=speed.speed_kmh * consts.KMH_TO_MS
        ))

    return speed_map


def load_path(shape: models.Shape, reverse: bool = False) -> Path:
    point_objs: typing.List[models.ShapePoint] = list(shape.points.order_by('order').all())
    points = [Point(long=p.longitude, lat=p.latitude) for p in point_objs]

    if reverse:
        points = points[::-1]

    speeds = []
    for p in point_objs[:-1]:
        speeds.append(Speed(
            monday=map_point_speed(list(p.average_speeds.filter(valid_monday=True))),
            tuesday=map_point_speed(list(p.average_speeds.filter(valid_tuesday=True))),
            wednesday=map_point_speed(list(p.average_speeds.filter(valid_wednesday=True))),
            thursday=map_point_speed(list(p.average_speeds.filter(valid_thursday=True))),
            friday=map_point_speed(list(p.average_speeds.filter(valid_friday=True))),
            saturday=map_point_speed(list(p.average_speeds.filter(valid_saturday=True))),
            sunday=map_point_speed(list(p.average_speeds.filter(valid_sunday=True))),
            limit_ms=p.speed_limit_kmh * consts.KMH_TO_MS
        ))

    path = Path(
        points=points,
        speeds=speeds
    )
    path.calculate_distances()
    return path


class VehicleState(enum.Enum):
    UNKNOWN = enum.auto()
    AT_STOP = enum.auto()
    BETWEEN_STOPS = enum.auto()


@dataclasses.dataclass
class UpdateState:
    vehicle: models.Vehicle
    now: datetime.datetime
    position: Point
    velocity: float = 0
    journey: typing.Optional[models.Journey] = None
    current_point: typing.Optional[models.JourneyPoint] = None
    path: typing.Optional[Path] = None


@shared_task(bind=True, ignore_result=True)
def vehicle_report(self, vehicle_id: str):
    """Updates the vehicle arrival estimator based on the latest position report"""

    vehicle = models.Vehicle.objects.get(id=vehicle_id)
    last_position = vehicle.positions.order_by("-timestamp").first()
    if last_position is None:
        return

    now = last_position.timestamp.astimezone(datetime.timezone.utc)
    position_point = Point(long=last_position.longitude, lat=last_position.latitude)
    update_state = UpdateState(
        vehicle=vehicle,
        now=now,
        position=position_point,
        velocity=last_position.velocity_ms
    )
    update_vehicle_journey_from_report(self.app.oid, update_state)


@shared_task(ignore_result=True)
def update_journey_estimates():
    now = timezone.now()
    active_journeys = models.Journey.objects.filter(
        real_time_state=models.Journey.RT_STATE_ACTIVE
    )
    for journey in active_journeys:
        update_vehicle_journey_from_estimate(journey.id, int(now.timestamp()))


@shared_task(bind=True, ignore_result=True)
def update_vehicle_journey_from_estimate(self, journey_id: str, now: int):
    now = datetime.datetime.fromtimestamp(now, tz=datetime.timezone.utc)
    journey = models.Journey.objects.get(id=journey_id)

    with memcache_lock(f"journey_update_{journey.id}", self.app.oid) as acquired:
        if not acquired:
            logging.info(f"Update lock on journey {journey} held elsewhere")
            return

        kalman_distance_to_next_stop = kalman_filter_distance_to_next_stop(
            journey, now, None, None
        )
        if kalman_distance_to_next_stop is None:
            return

        if journey.vehicle:
            logging.info(f"Vehicle {journey.vehicle} kalman estimate distance to next stop: "
                         f"{kalman_distance_to_next_stop:.2f}m")

        next_stop = journey.points.filter(
            real_time_arrival__isnull=True
        ).order_by('order').first()
        if not next_stop:
            return

        path = load_path(journey.shape, reverse=journey.direction == models.Journey.DIRECTION_OUTBOUND)

        if kalman_distance_to_next_stop <= 0:
            time_next_stop = now
        else:
            time_next_stop = distance_to_next_stop_to_travel_time(
                path=path, next_point=Point(lat=next_stop.stop.latitude, long=next_stop.stop.longitude),
                distance_to_next_stop=kalman_distance_to_next_stop, now=now
            )
            if journey.vehicle:
                logging.info(f"Vehicle {journey.vehicle} arrival time at next stop: {time_next_stop}")

        last_stop = journey.points.order_by('order').last()

        next_stop.estimated_arrival = time_next_stop.time()
        if next_stop != last_stop:
            next_stop.estimated_departure = estimate_departure_time_from_stop(now, next_stop).time()
        next_stop.save()

        if journey.vehicle:
            log_estimates(journey.vehicle, next_stop)

        update_future_stops_arrival_time(
            journey=journey, vehicle=journey.vehicle, path=path, start_stop=next_stop,
            now=now
        )


def update_vehicle_journey_from_report(oid, update_state: UpdateState):
    update_state.journey = models.Journey.objects.filter(
        vehicle=update_state.vehicle,
        date=update_state.now.date(),
        real_time_state=models.Journey.RT_STATE_ACTIVE
    ).first()

    # Does the vehicle have a currently active journey?
    if not update_state.journey:
        logging.info(f"No active journey for vehicle {update_state.vehicle}; attempting to find stop to start journey from")
        find_current_journey(update_state)

        if not update_state.journey:
            logging.info(f"Cannot find journey for vehicle {update_state.vehicle}")
            return

    while True:
        with memcache_lock(f"journey_update_{update_state.journey.id}", oid) as acquired:
            if not acquired:
                logging.info(f"Update lock on journey {update_state.journey} held elsewhere")
                time.sleep(1)
                continue

            # If we don't have know that the vehicle is currently at a stop, find out if it is
            if not update_state.current_point:
                update_state.current_point = find_current_journey_point(update_state)

            # If the vehicle is at a stop, update the real-time arrival time if it is not already set
            if update_state.current_point:
                if not update_state.current_point.real_time_arrival:
                    update_state.current_point.real_time_arrival = update_state.now.time()
                    update_state.current_point.estimated_arrival = None
                    update_state.current_point.save()

            with transaction.atomic():
                # Is the current stop the last stop on the journey
                if update_state.journey.points.order_by('order').last() == update_state.current_point:
                    logging.info(f"Journey completed for vehicle {update_state.vehicle}: {update_state.journey}")
                    # Mark the journey as finished
                    update_state.journey.real_time_state = models.Journey.RT_STATE_COMPLETED
                    update_state.journey.kalman_estimator_state = None
                    update_state.journey.save()

                    # Does the vehicle have another journey to start?
                    forms_into = update_state.journey.forms_into_opt()
                    if forms_into:
                        # Set the vehicle's next journey as active
                        forms_into.real_time_state = models.Journey.RT_STATE_ACTIVE
                        forms_into.save()
                        update_state.journey = forms_into

                        # Is the vehicle currently at a stop on its next journey?
                        update_state.current_point = find_current_journey_point(update_state)
                        if update_state.current_point:
                            update_state.current_point.real_time_arrival = update_state.now.time()
                            update_state.current_point.estimated_arrival = None
                            update_state.current_point.save()
                    else:
                        # If the vehicle doesn't have a next journey, we are done
                        return

            if not update_state.journey.shape:
                logging.info(f"No shape for journey, can't update stop arrival estimates: {update_state.journey}")
                return

            if update_state.journey.shape.points.count() == 0:
                logging.info(f"Empty shape for journey, can't update stop arrival estimates: {update_state.journey}")
                return

            update_state.path = load_path(
                update_state.journey.shape,
                reverse=update_state.journey.direction == models.Journey.DIRECTION_OUTBOUND
            )

            # If the vehicle is at a stop, we are done
            if update_state.current_point:

                # Estimator state is only used between stops
                update_state.journey.kalman_estimator_state = None
                update_state.journey.save()

                # Update the estimate for when the vehicle with leave the current stop
                departure_time = estimate_departure_time_from_stop(update_state.now, update_state.current_point)
                update_state.current_point.estimated_departure = departure_time.time()
                update_state.current_point.save()

                log_estimates(update_state.vehicle, update_state.current_point)

                update_future_stops_arrival_time(
                    journey=update_state.journey, vehicle=update_state.vehicle, path=update_state.path,
                    start_stop=update_state.current_point, now=departure_time
                )
            # If the vehicle is not at a stop, we need to update its distance to the next stop
            else:
                last_stop = update_state.journey.points.filter(
                    real_time_arrival__isnull=False
                ).order_by('order').last()
                next_stop = update_state.journey.points.filter(
                    order__gt=last_stop.order
                ).order_by('order').first()
                if not next_stop:
                    return

                update_in_between_stops_estimate(update_state, last_stop, next_stop)

            break


def select_journey_point(
        update_state: UpdateState, points: typing.List[models.JourneyPoint], date: datetime.date = None
) -> typing.Optional[models.JourneyPoint]:
    """Searches for a stop that is within the search radius of the vehicle's current position and has the closest
     planned arrival / departure time to the current time."""

    date = date or update_state.journey.date

    candidate_points = []
    for stop in points:
        stop_time = stop.departure_time
        if not stop_time:
            stop_time = stop.arrival_time

        stop_time = datetime.datetime.combine(date, stop_time).astimezone(datetime.timezone.utc)

        candidate_points.append({
            "abs_time_delta": abs((stop_time - update_state.now).total_seconds()),
            "point": Point(long=stop.stop.longitude, lat=stop.stop.latitude),
            "obj": stop
        })

    candidate_points.sort(key=lambda x: x["abs_time_delta"])

    selected_point = None
    for stop in candidate_points:
        if update_state.position.distance_to(stop["point"]) < STOP_SEARCH_RADIUS_METERS:
            selected_point = stop
            break

    return selected_point["obj"] if selected_point else None


def find_current_journey_point(update_state: UpdateState) -> typing.Optional[models.JourneyPoint]:
    """Finds the current stop that a vehicle is at"""

    return select_journey_point(update_state, update_state.journey.points.filter(
        real_time_departure__isnull=True
    ))


def estimate_departure_time_from_stop(now: datetime.datetime, stop: models.JourneyPoint) -> datetime.datetime:
    arrival_time = datetime.datetime.combine(
        now.date(),
        stop.real_time_arrival if stop.real_time_arrival else (
            stop.estimated_arrival if stop.estimated_arrival else (
                stop.arrival_time if stop.arrival_time else stop.departure_time
            )
        )
    )

    possible_departure_times = [arrival_time + MINIMUM_STOP_TIME]
    if stop.timing_point:
        if stop.departure_time:
            possible_departure_times.append(datetime.datetime.combine(now.date(), stop.departure_time))
        if stop.arrival_time:
            t = datetime.datetime.combine(now.date(), stop.arrival_time)
            possible_departure_times.append(t + MINIMUM_STOP_TIME)

    return max(possible_departure_times)


def update_in_between_stops_estimate(
        update_state: UpdateState, prev_stop: models.JourneyPoint, next_stop: models.JourneyPoint
):
    logging.info(f"Vehicle {update_state.vehicle} currently between stops: {prev_stop.stop} - {next_stop.stop}")

    if not prev_stop.real_time_departure:
        prev_stop.real_time_departure = update_state.now
        prev_stop.estimated_departure = None
        prev_stop.save()

    next_point = Point(long=next_stop.stop.longitude, lat=next_stop.stop.latitude)
    path_start_point_idx, distance_along_start_segment = \
        find_point_on_path(update_state.position, update_state.path)
    path_end_point_idx, distance_along_end_segment = find_point_on_path(next_point, update_state.path)

    if path_start_point_idx >= path_end_point_idx:
        logging.info(f"Vehicle {update_state.vehicle} has passed stop {next_stop.stop} without updates")
        next_stop.real_time_arrival = update_state.now.time()
        next_stop.estimated_arrival = None
        next_stop.save()

        prev_stop = next_stop
        next_stop = update_state.journey.points.filter(
            order__gt=prev_stop.order
        ).order_by('order').first()
        if next_stop:
            update_in_between_stops_estimate(update_state, prev_stop, next_stop)

        return

    distance_to_next_stop = update_state.path.distances[path_start_point_idx] * distance_along_start_segment
    i = path_start_point_idx + 1
    while i != path_end_point_idx:
        distance_to_next_stop += update_state.path.distances[i]
        i += 1
    if path_end_point_idx + 1 != len(update_state.path.points):
        distance_to_next_stop += update_state.path.distances[path_end_point_idx ] * distance_along_end_segment

    logging.info(f"Vehicle {update_state.vehicle} distance to next stop: {distance_to_next_stop:.2f}m")

    kalman_distance_to_next_stop = kalman_filter_distance_to_next_stop(
        journey=update_state.journey, now=update_state.now, last_known_velocity=update_state.velocity,
        known_distance_to_next_stop=distance_to_next_stop
    )
    logging.info(f"Vehicle {update_state.vehicle} kalman estimate distance to next stop: {kalman_distance_to_next_stop:.2f}m")

    time_next_stop = distance_to_next_stop_to_travel_time(
        path=update_state.path, next_point=next_point, distance_to_next_stop=kalman_distance_to_next_stop,
        now=update_state.now
    )

    last_stop = update_state.journey.points.order_by('order').last()

    next_stop.estimated_arrival = time_next_stop.time()
    if next_stop != last_stop:
        next_stop.estimated_departure = estimate_departure_time_from_stop(update_state.now, next_stop).time()
    next_stop.save()

    log_estimates(update_state.vehicle, next_stop)

    update_future_stops_arrival_time(
        journey=update_state.journey, vehicle=update_state.vehicle, path=update_state.path, start_stop=next_stop,
        now=update_state.now
    )


def kalman_filter_distance_to_next_stop(
        journey: models.Journey,
        now: datetime.datetime,
        last_known_velocity: typing.Optional[float],
        known_distance_to_next_stop: typing.Optional[float]
) -> typing.Optional[float]:
    t = int(now.timestamp())

    if not journey.kalman_estimator_state:
        if not last_known_velocity or not known_distance_to_next_stop:
            return None

        journey.kalman_estimator_state = {
            "p": 0,
            "x": known_distance_to_next_stop,
            "u": last_known_velocity,
            "t": t,
        }
        journey.save()

        return known_distance_to_next_stop
    else:
        if known_distance_to_next_stop:
            p_prev = journey.kalman_estimator_state["p"]
            x_prev = journey.kalman_estimator_state["x"]

            p1 = p_prev + GPS_VARIANCE
            b = p1 * (1/(p1 + GPS_VARIANCE))
            p = p1 - b * p1
            x = x_prev + b * (known_distance_to_next_stop - x_prev)

            journey.kalman_estimator_state = {
                "p": p,
                "x": x,
                "u": last_known_velocity or journey.kalman_estimator_state["u"],
                "t": t,
            }
            journey.save()

            return x
        else:
            if journey.kalman_estimator_state["x"] <= 0:
                return 0

            t_delta = t - journey.kalman_estimator_state["t"]
            journey.kalman_estimator_state = {
                "x": journey.kalman_estimator_state["x"] - t_delta * journey.kalman_estimator_state["u"],
                "p": journey.kalman_estimator_state["p"] + GPS_VARIANCE,
                "u": journey.kalman_estimator_state["u"],
                "t": t,
            }
            journey.save()

            return max(journey.kalman_estimator_state["x"], 0)


def distance_to_next_stop_to_travel_time(
        path: Path, next_point: Point, distance_to_next_stop: float, now: datetime.datetime
) -> datetime.datetime:
    path_end_point_idx, distance_along_end_segment = find_point_on_path(next_point, path)

    if path_end_point_idx == len(path.points) - 1:
        distance = 0
    else:
        distance = path.distances[path_end_point_idx] * distance_along_end_segment

    i = path_end_point_idx - 1
    while distance < distance_to_next_stop:
        distance += path.distances[i]

    if distance == distance_to_next_stop:
        distance_along_start_segment = 0
    else:
        distance_along_start_segment = (distance - distance_to_next_stop) - path.distances[i]

    return estimate_time_along_path_segment(
        path=path, now=now, start_point_idx=i, end_point_idx=path_end_point_idx,
        distance_along_start_segment=distance_along_start_segment,
        distance_along_end_segment=distance_along_end_segment
    )


def find_current_journey(update_state: UpdateState):
    journeys_on_date = list(models.Journey.objects.filter(
        vehicle=update_state.vehicle,
        date=update_state.now.date()
    ))

    if not journeys_on_date:
        logging.info(f"No journeys on date for vehicle - {update_state.vehicle}")
        return

    selected_point = select_journey_point(update_state, models.JourneyPoint.objects.filter(
        journey__in=journeys_on_date,
        real_time_departure__isnull=True
    ), date=update_state.now.date())

    if selected_point is None:
        logging.info(f"Cannot find current journey point for vehicle - {update_state.vehicle}")
        return

    logging.info(f"Found current journey point for vehicle - {update_state.vehicle} - {selected_point}")

    current_journey = selected_point.journey
    current_journey.real_time_state = models.Journey.RT_STATE_ACTIVE
    current_journey.save()

    update_state.current_point = selected_point
    update_state.journey = current_journey


def find_point_on_path(search_point: Point, path: Path) -> typing.Tuple[int, float]:
    closest_points = path.get_closest_points(search_point, k=3)

    line_candidates = []
    for point, point_idx in closest_points:
        if point_idx + 1 == len(path.points):
            end_point = path.points[point_idx - 1]
        else:
            end_point = path.points[point_idx + 1]

        line = shapely.LineString([point.point, end_point.point])
        distance = shapely.hausdorff_distance(line, search_point.point, densify=0.5)
        line_candidates.append((line, point_idx, distance))

    line_candidates.sort(key=lambda x: x[2])
    closest_line, point_idx, _ = line_candidates[0]
    distance_along_segment = closest_line.project(search_point.point, normalized=True)

    return point_idx, distance_along_segment


def update_future_stops_arrival_time(
        journey: models.Journey, vehicle: typing.Optional[models.Vehicle], path: Path,
        start_stop: models.JourneyPoint, now: datetime.datetime
):
    next_stop: typing.Optional[models.JourneyPoint] = journey.points.filter(
        order__gt=start_stop.order
    ).order_by('order').first()
    last_stop = journey.points.order_by('order').last()
    if not next_stop:
        return

    start_point = Point(long=start_stop.stop.longitude, lat=start_stop.stop.latitude)
    next_point = Point(long=next_stop.stop.longitude, lat=next_stop.stop.latitude)

    path_start_point_idx, distance_along_start_segment = find_point_on_path(start_point, path)
    path_end_point_idx, distance_along_end_segment = find_point_on_path(next_point, path)

    estimate_timestamp = estimate_departure_time_from_stop(now, start_stop)
    estimate_timestamp = estimate_time_along_path_segment(
        path, estimate_timestamp, path_start_point_idx, path_end_point_idx,
        distance_along_start_segment, distance_along_end_segment
    )

    next_stop.estimated_arrival = estimate_timestamp.time()
    if next_stop != last_stop:
        next_time = estimate_departure_time_from_stop(now, next_stop)
        next_stop.estimated_departure = next_time.time()
    else:
        next_time = estimate_timestamp
        next_stop.estimated_departure = None
    next_stop.save()

    if vehicle:
        log_estimates(vehicle, next_stop)

    update_future_stops_arrival_time(
        journey=journey, vehicle=vehicle, path=path, start_stop=next_stop, now=next_time
    )


def travel_time_segment(path: Path, start_point_idx: int, now: datetime.datetime, fraction: float = 1) -> float:
    speed_start_segment = path.speeds[start_point_idx].average_speed_at_time(now)
    travel_time_start_segment = (path.distances[start_point_idx] * fraction) / speed_start_segment
    return travel_time_start_segment


def estimate_time_along_path_segment(
        path: Path,
        now: datetime.datetime,
        start_point_idx: int,
        end_point_idx: int,
        distance_along_start_segment: float = 0,
        distance_along_end_segment: float = 1,
) -> datetime.datetime:
    travel_time_start_segment = travel_time_segment(
        path, start_point_idx, now, (1 - distance_along_start_segment)
    )
    now += datetime.timedelta(seconds=travel_time_start_segment)
    i = start_point_idx + 1
    while i != end_point_idx:
        travel_time = travel_time_segment(path, i, now)
        now += datetime.timedelta(seconds=travel_time)
        i += 1

    if end_point_idx + 1 != len(path.points):
        travel_time_end_segment = travel_time_segment(
            path, end_point_idx, now, distance_along_end_segment
        )
        now += datetime.timedelta(seconds=travel_time_end_segment)

    return now


def log_estimates(vehicle: models.Vehicle, stop: models.JourneyPoint):
    logging.info(f"Estimated times for vehicle {vehicle} at stop {stop.stop}: "
                 f"plan arr {stop.arrival_time if stop.arrival_time else 'X'} "
                 f"plan dep {stop.departure_time if stop.arrival_time else 'X'}; "
                 f"est arr {stop.estimated_arrival if stop.estimated_arrival else 'X'} "
                 f"est dep {stop.estimated_departure if stop.estimated_departure else 'X'}")
