class SeverityAnalyzer:

    def analyze(
        self,
        scenario
    ):

        vehicle_speed = (
            scenario[
                "traffic"
            ][
                "average_speed"
            ]
        )

        weather = (
            scenario[
                "weather"
            ][
                "condition"
            ]
        )

        corner_case = (
            scenario[
                "corner_case"
            ][
                "type"
            ]
        )

        # 매우 위험한 상황
        if (
            vehicle_speed > 60
            and weather in [
                "heavy_rain",
                "fog",
                "night_rain"
            ]
        ):
            return "S3"

        if (
            corner_case in [
                "blind_spot_pedestrian",
                "wrong_way_vehicle"
            ]
        ):
            return "S3"

        # 중간 위험
        if vehicle_speed > 40:
            return "S2"

        # 낮은 위험
        return "S1"