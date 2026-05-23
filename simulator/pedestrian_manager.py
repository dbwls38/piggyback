import carla


class EnvironmentManager:

    def __init__(
        self,
        world
    ):

        self.world = world

    def set_clear_weather(self):

        weather = (
            carla.WeatherParameters(
                cloudiness=10,
                precipitation=0,
                fog_density=0,
                wetness=0
            )
        )

        self.world.set_weather(
            weather
        )

        print()

        print(
            "[WEATHER] CLEAR"
        )

    def set_rain_weather(self):

        weather = (
            carla.WeatherParameters(
                cloudiness=90,
                precipitation=80,
                fog_density=20,
                wetness=90
            )
        )

        self.world.set_weather(
            weather
        )

        print()

        print(
            "[WEATHER] RAIN"
        )

    def set_night_rain(self):

        weather = (
            carla.WeatherParameters(
                cloudiness=100,
                precipitation=90,
                fog_density=40,
                wetness=100,
                sun_altitude_angle=-90
            )
        )

        self.world.set_weather(
            weather
        )

        print()

        print(
            "[WEATHER] NIGHT RAIN"
        )