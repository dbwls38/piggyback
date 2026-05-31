class TTCCalculator:

    @staticmethod
    def calculate(
        distance,
        relative_speed
    ):

        if relative_speed <= 0:
            return float("inf")

        return distance / relative_speed


class RiskQuantifier:

    def quantify(
        self,
        ttc,
        visibility
    ):

        score = 0

        # TTC 기반 위험도

        if ttc < 1:
            score += 50

        elif ttc < 2:
            score += 35

        elif ttc < 4:
            score += 20

        # Visibility 기반 위험도

        if visibility < 15:
            score += 30

        elif visibility < 30:
            score += 20

        elif visibility < 50:
            score += 10

        return score


class SaraEngine:

    def __init__(
        self,
        critical_threshold=1.0,
        dangerous_threshold=3.0
    ):

        self.critical_threshold = (
            critical_threshold
        )

        self.dangerous_threshold = (
            dangerous_threshold
        )

    def assess(
        self,
        ttc
    ):

        if ttc < self.critical_threshold:
            return "CRITICAL"

        if ttc < self.dangerous_threshold:
            return "DANGEROUS"

        return "SAFE"


class ControllabilityClassifier:

    def classify(
        self,
        ttc,
        risk_score,
        visibility
    ):

        # 매우 위험

        if (
            ttc < 1
            or risk_score >= 80
            or visibility < 15
        ):
            return "C3"

        # 위험

        if (
            ttc < 3
            or risk_score >= 50
            or visibility < 30
        ):
            return "C2"

        # 제어 가능

        return "C1"