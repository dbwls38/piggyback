import random

class WeatherGenerator:
    def generate(self):
        weather_conditions = [
            "clear",
            "rain",
            "heavy_rain",
            "fog",
            "night",
            "night_rain"
        ]

        selected_weather = (
            random.choice(
                weather_conditions
            )
        )

        weather = {
            "condition":
                selected_weather,

            "visibility_distance":
                random.randint(
                    10,
                    100
                ),

            "road_friction":
                round(
                    random.uniform(
                        0.3,
                        1.0
                    ),
                    2
                )
        }

        return weather