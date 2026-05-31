from hara.iso26262_table import ASIL_TABLE


class TTCCalculator:

    @staticmethod
    def calculate(
        distance,
        relative_speed
    ):

        if relative_speed <= 0:
            return float("inf")

        return distance / relative_speed


class ControllabilityClassifier:

    def classify(self, ttc):

        if ttc < 1:
            return "C3"

        if ttc < 3:
            return "C2"

        return "C1"


class SeverityAnalyzer:

    def analyze(
        self,
        scenario
    ):

        vehicle_speed = (
            scenario["traffic"]["average_speed"]
        )

        weather = (
            scenario["weather"]["condition"]
        )

        corner_case = (
            scenario["corner_case"]["type"]
        )

        if (
            vehicle_speed > 60
            and weather in [
                "heavy_rain",
                "fog",
                "night_rain"
            ]
        ):
            return "S3"

        if corner_case in [
            "blind_spot_pedestrian",
            "wrong_way_vehicle"
        ]:
            return "S3"

        if vehicle_speed > 40:
            return "S2"

        return "S1"


class DynamicExposureModel:

    def calculate(
        self,
        scenario
    ):

        score = 0

        traffic_density = (
            scenario["traffic"]["vehicle_density"]
        )

        weather = (
            scenario["weather"]["condition"]
        )

        pedestrian_behavior = (
            scenario["pedestrian"]["behavior"]
        )

        if traffic_density > 40:
            score += 3

        elif traffic_density > 20:
            score += 2

        else:
            score += 1

        if weather in [
            "heavy_rain",
            "fog",
            "night_rain"
        ]:
            score += 2

        if pedestrian_behavior in [
            "jaywalking",
            "sudden_run"
        ]:
            score += 2

        if score >= 6:
            return "E4"

        if score >= 4:
            return "E3"

        if score >= 2:
            return "E2"

        return "E1"


class ASILClassifier:

    def classify(
        self,
        severity,
        exposure,
        controllability
    ):

        key = (
            severity,
            exposure,
            controllability
        )

        return ASIL_TABLE.get(
            key,
            "QM"
        )


class SafetyGoalGenerator:

    def generate(
        self,
        hara_result
    ):

        asil = hara_result["asil"]

        if asil == "ASIL-D":

            return {
                "goal":
                    "Prevent pedestrian collision during right-turn Testscenarios.",
                "requirement":
                    "Emergency braking must activate within 300ms."
            }

        if asil == "ASIL-C":

            return {
                "goal":
                    "Reduce collision probability.",
                "requirement":
                    "Driver warning required."
            }

        return {
            "goal":
                "Maintain safe driving.",
            "requirement":
                "Standard monitoring."
        }


class HARAEngine:

    def evaluate(
        self,
        scenario,
        distance,
        relative_speed
    ):

        ttc = TTCCalculator.calculate(
            distance,
            relative_speed
        )

        severity = (
            SeverityAnalyzer()
            .analyze(scenario)
        )

        exposure = (
            DynamicExposureModel()
            .calculate(scenario)
        )

        controllability = (
            ControllabilityClassifier()
            .classify(ttc)
        )

        asil = (
            ASILClassifier()
            .classify(
                severity,
                exposure,
                controllability
            )
        )

        return {
            "ttc": ttc,
            "severity": severity,
            "exposure": exposure,
            "controllability": controllability,
            "asil": asil
        }
