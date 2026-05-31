# generators/corner_case.py
import random

class CornerCaseGenerator:

    def generate(self):

        return {
            "type": random.choice([
                "pedestrian_occlusion",
                "sudden_vehicle_cutin",
                "sensor_failure",
                "traffic_light_failure",
                "blind_spot_pedestrian",
                "unexpected_braking",
                "wrong_way_vehicle"
            ]),
            "risk_level": random.choice([
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL"
            ])
        }