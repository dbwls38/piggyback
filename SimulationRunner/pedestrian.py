# generators/pedestrian.py
import random

class PedestrianBehaviorAI:

    def generate(self):

        return {
            "behavior": random.choice([
                "normal_crossing",
                "jaywalking",
                "sudden_run",
                "phone_distracted",
                "slow_crossing"
            ]),
            "speed": round(random.uniform(0.5, 2.5), 2),
            "visibility": random.choice(["high", "medium", "low"])
        }