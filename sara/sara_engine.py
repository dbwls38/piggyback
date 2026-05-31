class TTCCalculator:

    @staticmethod
    def calculate(
        distance,
        relative_speed
    ):

        if relative_speed <= 0:
            return float("inf")

        return distance / relative_speed


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

    def assess(self, ttc):

        if ttc < self.critical_threshold:
            return "CRITICAL"

        if ttc < self.dangerous_threshold:
            return "DANGEROUS"

        return "SAFE"


class ControllabilityClassifier:

    def classify(self, ttc):

        if ttc < 1:
            return "C3"

        if ttc < 3:
            return "C2"

        return "C1"