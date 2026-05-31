import random
import time
class RadarSensor:

    def __init__(
        self,
        max_distance=100,
        field_of_view=120,
        update_rate=0.1
    ):

        self.max_distance = max_distance

        self.field_of_view = field_of_view

        self.update_rate = update_rate

        self.detected_objects = []

    def initialize(self):

        print()

        print("================================")
        print(" RADAR SENSOR INITIALIZED ")
        print("================================")

        print(
            f"Max Distance: "
            f"{self.max_distance} m"
        )

        print(
            f"Field of View: "
            f"{self.field_of_view} deg"
        )

        print(
            f"Update Rate: "
            f"{self.update_rate} sec"
        )

    def scan(self):

        self.detected_objects = []

        object_count = random.randint(
            1,
            5
        )

        for obj_id in range(object_count):

            detected_object = {

                "id":
                    obj_id,

                "distance":
                    round(
                        random.uniform(0,100),
                        2
                    ),

                "relative_speed":
                    round(
                        random.uniform(
                            -25,
                            25
                        ),
                        2
                    ),

                "angle":
                    round(
                        random.uniform(
                            -self.field_of_view / 2,
                            self.field_of_view / 2
                        ),
                        2
                    ),

                "signal_strength":
                    round(
                        random.uniform(
                            0.5,
                            1.0
                        ),
                        2
                    )
            }

            self.detected_objects.append(
                detected_object
            )

        return self.detected_objects

    def filter_objects(
        self,
        min_distance=1,
        max_distance=50
    ):

        filtered = []

        for obj in self.detected_objects:

            if (
                min_distance
                <= obj["distance"]
                <= max_distance
            ):

                filtered.append(obj)

        return filtered

    def get_closest_object(self):

        if not self.detected_objects:

            return None

        closest = min(
            self.detected_objects,
            key=lambda obj:
            obj["distance"]
        )

        return closest

    def monitor(
        self,
        duration=5
    ):

        print()

        print("================================")
        print(" RADAR MONITORING START ")
        print("================================")

        start_time = time.time()

        while (
            time.time() - start_time
            < duration
        ):

            objects = self.scan()

            print()

            print(
                f"[SCAN] "
                f"{len(objects)} objects detected"
            )

            for obj in objects:

                print(
                    f"ID={obj['id']} | "
                    f"Dist={obj['distance']}m | "
                    f"RelSpeed={obj['relative_speed']}m/s | "
                    f"Angle={obj['angle']}deg"
                )

            time.sleep(
                self.update_rate
            )

        print()

        print("================================")
        print(" RADAR MONITORING END ")
        print("================================")


if __name__ == "__main__":

    radar = RadarSensor(
        max_distance=120,
        field_of_view=140,
        update_rate=1
    )

    radar.initialize()

    detected = radar.scan()

    print()

    print("===== DETECTED OBJECTS =====")

    for obj in detected:

        print(obj)

    print()

    print("===== FILTERED OBJECTS =====")

    filtered = radar.filter_objects(
        min_distance=5,
        max_distance=40
    )

    for obj in filtered:

        print(obj)

    print()

    print("===== CLOSEST OBJECT =====")

    closest = radar.get_closest_object()

    print(closest)

    radar.monitor(duration=3)