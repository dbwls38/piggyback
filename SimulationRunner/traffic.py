# generators/traffic.py
import random

class TrafficGenerator:

    def generate(self):

        return {
            "pattern": random.choice([
                "light",
                "moderate",
                "heavy",
                "aggressive_cutin",
                "signal_violation"
            ]),
            "vehicle_density": random.randint(5, 50),
            "average_speed": random.randint(20, 80)
        }