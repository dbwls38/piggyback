import random


class CornerCaseGenerator:

    def generate(self):

        corner_cases = [

            "pedestrian_occlusion",

            "sudden_vehicle_cutin",

            "sensor_failure",

            "traffic_light_failure",

            "blind_spot_pedestrian",

            "unexpected_braking",

            "wrong_way_vehicle"
        ]

        selected_case = (
            random.choice(
                corner_cases
            )
        )

        risk_level = (
            random.choice([
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL"
            ])
        )

        corner_case = {

            "type":
                selected_case,

            "risk_level":
                risk_level
        }

        return corner_case