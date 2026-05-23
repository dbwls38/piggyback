import random


class TrafficPatternGenerator:

    def generate(self):

        traffic_patterns = [

            "light",

            "moderate",

            "heavy",

            "aggressive_cutin",

            "signal_violation"
        ]

        selected_pattern = (
            random.choice(
                traffic_patterns
            )
        )

        traffic = {

            "pattern":
                selected_pattern,

            "vehicle_density":
                random.randint(
                    5,
                    50
                ),

            "average_speed":
                random.randint(
                    20,
                    80
                )
        }

        return traffic