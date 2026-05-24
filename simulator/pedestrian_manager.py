import random

class PedestrianManager:

    def __init__(
        self,
        client
    ):

        self.client = client

        self.pedestrians = []

    # =====================================
    # SPAWN PEDESTRIAN
    # =====================================

    def spawn_pedestrian(self):

        pedestrian = {

            "id":
                len(self.pedestrians) + 1,

            "position": {

                "x":
                    random.randint(5, 25),

                "y":
                    random.randint(-5, 5)
            },

            "speed":
                round(
                    random.uniform(
                        0.5,
                        2.0
                    ),
                    2
                ),

            "crossing":
                True,

            "detected":
                False
        }

        self.pedestrians.append(
            pedestrian
        )

        print()

        print(
            "[PEDESTRIAN SPAWNED]"
        )

        print(pedestrian)

        return pedestrian

    # =====================================
    # UPDATE PEDESTRIANS
    # =====================================

    def update(self):

        for pedestrian in (
            self.pedestrians
        ):

            pedestrian["position"][
                "x"
            ] -= pedestrian[
                "speed"
            ] * 0.1

    # =====================================
    # GET PEDESTRIANS
    # =====================================

    def get_pedestrians(self):

        return self.pedestrians

    # =====================================
    # SIMULATE JAYWALKING
    # =====================================

    def simulate_jaywalking(self):

        pedestrian = (
            self.spawn_pedestrian()
        )

        pedestrian["jaywalking"] = True

        print()

        print(
            "[JAYWALKING EVENT]"
        )

        return pedestrian

    # =====================================
    # CORNER CASE EVENT
    # =====================================

    def sudden_crossing(self):

        pedestrian = {

            "id":
                len(self.pedestrians) + 1,

            "position": {
                "x": 3,
                "y": 0
            },

            "speed": 3.5,

            "crossing": True,

            "corner_case": True
        }

        self.pedestrians.append(
            pedestrian
        )

        print()

        print(
            "[CORNER CASE]"
        )

        print(
            "Sudden pedestrian crossing"
        )

        return pedestrian

    # =====================================
    # DESTROY ALL
    # =====================================

    def destroy_all(self):

        self.pedestrians.clear()

        print()

        print(
            "[ALL PEDESTRIANS REMOVED]"
        )
def apply_behavior(
    self,
    pedestrian
):

    print()

    print(
        "[PEDESTRIAN EVENT]"
    )

    print(
        pedestrian
    )

    behavior = (
        pedestrian["behavior"]
    )

    if behavior == "slow_crossing":

        print(
            "Pedestrian slowly crossing"
        )

    elif behavior == "jaywalking":

        print(
            "Jaywalking detected"
        )