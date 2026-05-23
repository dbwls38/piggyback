from sara.assess.ttc_calculator import (
    TTCCalculator
)

from sara.assess.collision_predictor import (
    CollisionPredictor
)

from sara.assess.risk_quantifier import (
    RiskQuantifier
)

from sara.assess.controllability_estimator import (
    ControllabilityEstimator
)


class SARAEngine:

    def __init__(self):

        self.ttc_calculator = (
            TTCCalculator()
        )

        self.collision_predictor = (
            CollisionPredictor()
        )

        self.risk_quantifier = (
            RiskQuantifier()
        )

        self.controllability_estimator = (
            ControllabilityEstimator()
        )

    def evaluate(
        self,
        detected_object,
        visibility
    ):

        distance = (
            detected_object[
                "distance"
            ]
        )

        relative_speed = (
            detected_object[
                "relative_speed"
            ]
        )

        ttc = (
            self.ttc_calculator.calculate(
                distance,
                relative_speed
            )
        )

        collision = (
            self.collision_predictor.predict(
                ttc
            )
        )

        risk_score = (
            self.risk_quantifier.quantify(
                ttc,
                collision[
                    "probability"
                ],
                visibility
            )
        )

        controllability = (
            self.controllability_estimator.estimate(
                ttc,
                risk_score,
                visibility
            )
        )

        return {

            "ttc":
                ttc,

            "collision_probability":
                collision[
                    "probability"
                ],

            "risk_level":
                collision[
                    "risk"
                ],

            "risk_score":
                risk_score,

            "controllability":
                controllability
        }