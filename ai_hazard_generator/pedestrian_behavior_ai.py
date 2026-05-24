import random
class PedestrianBehaviorAI:
    def generate(self):

        behaviors = [

            "normal_crossing",
            "jaywalking",
            "sudden_run",
            "phone_distracted",
            "slow_crossing"
        ]

        selected_behavior = (
            random.choice(behaviors)
        )

        pedestrian = {

            "behavior":
                selected_behavior,

            "speed":
                round(
                    random.uniform(0.5, 2.5),
                    2
                ),

            "visibility":
                random.choice([
                    "high",
                    "medium",
                    "low"
                ])
        }

        return pedestrian