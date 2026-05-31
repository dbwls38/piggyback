class NightRainScenario:

    def __init__(self):

        self.name = "night_rain"

    def spawn(self):

        print()

        print(
            "[SPAWN] Night rain"
        )

        self.environment = {

            "weather":
                "night_rain",

            "visibility":
                15
        }

        self.vehicle = {

            "speed":
                60
        }

    def run(self):

        print()

        print(
            "[RUNNING] Night rain"
        )

        return {

            "environment":
                self.environment,

            "vehicle":
                self.vehicle,

            "distance":
                18
        }
