class SensorFailureScenario:

    def __init__(self):

        self.name = (
            "sensor_failure"
        )

    def spawn(self):

        print()

        print(
            "[SPAWN] Sensor failure"
        )

        self.sensor = {

            "radar":
                False,

            "camera":
                False
        }

        self.vehicle = {

            "speed":
                50
        }

    def run(self):

        print()

        print(
            "[RUNNING] Sensor failure"
        )

        return {

            "sensor":
                self.sensor,

            "vehicle":
                self.vehicle,

            "distance":
                7
        }

    def evaluate(
        self,
        sara_result,
        hara_result
    ):

        print()

        print(
            "[CRITICAL SENSOR FAILURE]"
        )

        print(
            f"Controllability: "
            f"{hara_result['controllability']}"
        )

        print(
            f"ASIL: "
            f"{hara_result['asil']}"
        )