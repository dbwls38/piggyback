from hara.severity_analyzer import (
    SeverityAnalyzer
)
from hara.exposure_analyzer import (
    ExposureAnalyzer
)
from hara.controllability_mapper import (
    ControllabilityMapper
)
from hara.asil_classifier import (
    ASILClassifier
)

class HARAEngine:

    def __init__(self):

        self.severity_analyzer = (
            SeverityAnalyzer()
        )

        self.exposure_analyzer = (
            ExposureAnalyzer()
        )

        self.controllability_mapper = (
            ControllabilityMapper()
        )

        self.asil_classifier = (
            ASILClassifier()
        )

    def evaluate(
        self,
        scenario,
        sara_result
    ):

        severity = (
            self.severity_analyzer.analyze(
                scenario
            )
        )

        exposure = (
            self.exposure_analyzer.analyze(
                scenario
            )
        )

        controllability = (
            self.controllability_mapper.map(
                sara_result[
                    "controllability"
                ]
            )
        )

        asil = (
            self.asil_classifier.classify(
                severity,
                exposure,
                controllability
            )
        )

        return {

            "severity":
                severity,

            "exposure":
                exposure,

            "controllability":
                controllability,

            "asil":
                asil
        }