# generators/weather.py
import random

class WeatherGenerator:

    def generate(self):
        conditions = [
            "clear",
            "rain",
            "heavy_rain",
            "fog",
            "night",
            "night_rain"
        ]

        return {
            "condition": random.choice(conditions),
            "visibility_distance": random.randint(10, 100),
            "road_friction": round(random.uniform(0.3, 1.0), 2)
        }