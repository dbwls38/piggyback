class DynamicExposureModel:

    def calculate(
        self,
        scenario
    ):

        score = 0

        traffic_density = (
            scenario[
                "traffic"
            ][
                "vehicle_density"
            ]
        )

        weather = (
            scenario[
                "weather"
            ][
                "condition"
            ]
        )

        pedestrian_behavior = (
            scenario[
                "pedestrian"
            ][
                "behavior"
            ]
        )

        # 교통량 증가
        if traffic_density > 40:
            score += 3

        elif traffic_density > 20:
            score += 2

        else:
            score += 1

        # 악천후
        if weather in [
            "heavy_rain",
            "fog",
            "night_rain"
        ]:
            score += 2

        # 돌발 보행자
        if pedestrian_behavior in [
            "jaywalking",
            "sudden_run"
        ]:
            score += 2

        # Exposure 결정
        if score >= 6:
            return "E4"

        if score >= 4:
            return "E3"

        if score >= 2:
            return "E2"

        return "E1"