class RiskQuantifier:

    def quantify(
        self,
        ttc,
        collision_probability,
        visibility
    ):

        risk_score = 0

        # TTC 기반
        if ttc < 1:
            risk_score += 50

        elif ttc < 2:
            risk_score += 35

        elif ttc < 4:
            risk_score += 20

        # 충돌 확률
        risk_score += (
            collision_probability * 30
        )

        # 시야 감소
        if visibility < 20:
            risk_score += 20

        elif visibility < 50:
            risk_score += 10

        return round(
            risk_score,
            2
        )