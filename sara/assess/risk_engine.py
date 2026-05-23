import math

from sara.assess.ttc_calculator import TTCCalculator
from sara.assess.collision_predictor import CollisionPredictor
from sara.assess.safety_score import SafetyScore


class RiskEngine:
    def __init__(self):
        self.ttc_calculator = TTCCalculator()
        self.predictor = CollisionPredictor()
        self.score_engine = SafetyScore()

    def calculate_distance(self, loc1, loc2):
        dx = loc1.x - loc2.x
        dy = loc1.y - loc2.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def evaluate(
        self,
        vehicle_location,
        pedestrian_location,
        vehicle_velocity,
        pedestrian_velocity
    ):
        distance = self.calculate_distance(
            vehicle_location,
            pedestrian_location
        )

        relative_velocity = abs(
            vehicle_velocity - pedestrian_velocity
        )

        ttc = self.ttc_calculator.calculate(
            distance,
            relative_velocity
        )

        collision_probability = self.predictor.predict(ttc)

        score = self.score_engine.calculate(
            ttc,
            collision_probability
        )

        return {
            "distance": distance,
            "ttc": ttc,
            "collision_probability": collision_probability,
            "safety_score": score,
            "danger": ttc < 2
        }