import datetime
import json
import time
import django

IMEI = "300234011532400"


def main():
    import tracking.models
    import tracking.estimator

    tracker = tracking.models.Tracker.objects.get(imei=IMEI)

    with open("sim/sim_data.json", "r") as f:
        data = json.load(f)

    data.sort(key=lambda x: x["timestamp"])

    now = datetime.datetime(2024, 2, 24, 17, 20, 0)
    end = datetime.datetime(2024, 2, 24, 18, 0, 0)

    while now < end:
        if now.second == 0:
            print(f"Simulating {now}")

        # if now.second % 10 == 0:
        #     vehicle = tracker.vehicle_opt()
        #     if vehicle:
        #         print(f"Updating estimates at {now}")
        #         tracking.estimator.update_vehicle_journey_from_estimate.delay(str(vehicle.id), int(now.timestamp()))

        now_timestamp = now.timestamp()
        if data and data[0]["timestamp"] < now_timestamp:
            data_point = data.pop(0)
            data_time = datetime.datetime.fromtimestamp(data_point["timestamp"])
            print(f"Pushing update {data_time}: {data_point}")
            if tracker.vehicle:
                tracking.models.VehiclePosition(
                    vehicle=tracker.vehicle,
                    timestamp=data_time,
                    latitude=data_point["lat"],
                    longitude=data_point["long"],
                    velocity_ms=data_point["velocity"],
                ).save()
                tracking.estimator.vehicle_report.delay(str(vehicle.id))

        now += datetime.timedelta(seconds=5)
        time.sleep(0.3)


if __name__ == "__main__":
    django.setup()
    main()
