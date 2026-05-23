class SuddenCutInScenario:

    def __init__(self):

        self.name = (
            "sudden_cut_in"
        )

    def spawn(self):

        print()

        print(
            "[SPAWN] Sudden cut-in"
        )

        self.ego_vehicle = {

            "speed": 70
        }

        self.target_vehicle = {

            "cut_in":
                True,

            "speed":
                55
        }

    def run(self):

        print()

        print(
            "[RUNNING] Sudden cut-in"
        )

        return {

            "ego_vehicle":
                self.ego_vehicle,

            "target_vehicle":
                self.target_vehicle,

            "distance":
                10
        }

    def evaluate(
        self,
        sara_result,
        hara_result
    ):

        print()

        print(
            f"Collision Probability: "
            f"{sara_result['collision_probability']}"
        )

        print(
            f"ASIL: "
            f"{hara_result['asil']}"
        )