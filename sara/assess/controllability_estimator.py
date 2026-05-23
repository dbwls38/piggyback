class ControllabilityEstimator:

    def estimate(
        self,
        ttc,
        risk_score,
        visibility
    ):

        # 매우 위험
        if (
            ttc < 1
            or risk_score > 80
            or visibility < 15
        ):

            return "C3"

        # 중간 위험
        if (
            ttc < 2
            or risk_score > 50
        ):

            return "C2"

        # 제어 가능
        return "C1"