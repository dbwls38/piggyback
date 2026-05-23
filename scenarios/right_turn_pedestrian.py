class RightTurnPedestrianScenario:

    def __init__(self):

        self.name = (
            "right_turn_pedestrian"
        )

    def spawn(self):

        print()

        print(
            "[SPAWN] Right-turn scenario"
        )

        self.vehicle = {

            "speed": 35,

            "direction":
                "right_turn"
        }

        self.pedestrian = {

            "crossing":
                True,

            "speed":
                1.4
        }

    def run(self):

        print()

        print(
            "[RUNNING] Right-turn pedestrian scenario"
        )

        return {

            "vehicle":
                self.vehicle,

            "pedestrian":
                self.pedestrian,

            "distance":
                12
        }

    def evaluate(
        self,
        sara_result,
        hara_result
    ):

        print()

        print(
            "[EVALUATION]"
        )

        print(
            f"TTC: "
            f"{sara_result['ttc']}"
        )

        print(
            f"ASIL: "
            f"{hara_result['asil']}"
        )