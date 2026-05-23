class ExposureAnalyzer:

    def analyze(
        self,
        scenario
    ):

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

        if (
            traffic_density > 40
        ):
            return "E4"

        if weather in [
            "rain",
            "night_rain",
            "fog"
        ]:
            return "E3"

        if traffic_density > 20:
            return "E2"

        return "E1"