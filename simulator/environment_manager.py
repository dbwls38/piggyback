import airsim
class EnvironmentManager:
    def __init__(
        self,
        client
    ):

        self.client = client

        # Weather 시스템 활성화
        self.client.simEnableWeather(
            True
        )

    # =====================================
    # CLEAR WEATHER
    # =====================================

    def set_clear_weather(self):

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Rain,
            0.0
        )

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Fog,
            0.0
        )

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Roadwetness,
            0.0
        )

        print()

        print(
            "[WEATHER] CLEAR"
        )

    # =====================================
    # RAIN WEATHER
    # =====================================

    def set_rain_weather(self):

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Rain,
            0.8
        )

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Roadwetness,
            0.9
        )

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Fog,
            0.2
        )

        print()

        print(
            "[WEATHER] RAIN"
        )

    # =====================================
    # NIGHT RAIN
    # =====================================

    def set_night_rain(self):

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Rain,
            0.9
        )

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Roadwetness,
            1.0
        )

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Fog,
            0.4
        )

        # 야간 설정
        self.client.simSetTimeOfDay(
            True,
            "2025-01-01 22:00:00"
        )

        print()

        print(
            "[WEATHER] NIGHT RAIN"
        )

    # =====================================
    # FOG WEATHER
    # =====================================

    def set_fog_weather(self):

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Fog,
            0.8
        )

        self.client.simSetWeatherParameter(
            airsim.WeatherParameter.Rain,
            0.0
        )

        print()

        print(
            "[WEATHER] FOG"
        )