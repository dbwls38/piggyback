import airsim


class AirSimRunner:

    def __init__(self):

        self.client = airsim.CarClient()

        self.client.confirmConnection()

        self.client.enableApiControl(True)

        print()
        print("AirSim Connected")

    # =====================================
    # APPLY WEATHER
    # =====================================

    def apply_weather(
        self,
        weather
    ):

        self.client.simEnableWeather(
            True
        )

        weather_type = (
            weather["condition"]
        )

        print()
        print(
            f"Applying Weather: "
            f"{weather_type}"
        )

        # -------------------------
        # CLEAR
        # -------------------------

        if weather_type == "clear":

            self.client.simSetWeatherParameter(
                airsim.WeatherParameter.Rain,
                0.0
            )

            self.client.simSetWeatherParameter(
                airsim.WeatherParameter.Fog,
                0.0
            )

        # -------------------------
        # RAIN
        # -------------------------

        elif weather_type == "rain":

            self.client.simSetWeatherParameter(
                airsim.WeatherParameter.Rain,
                0.8
            )

            self.client.simSetWeatherParameter(
                airsim.WeatherParameter.Roadwetness,
                0.7
            )

        # -------------------------
        # FOG
        # -------------------------

        elif weather_type == "fog":

            self.client.simSetWeatherParameter(
                airsim.WeatherParameter.Fog,
                0.7
            )

        # -------------------------
        # NIGHT
        # -------------------------

        elif weather_type == "night":

            self.client.simSetTimeOfDay(
                True,
                "2025-01-01 22:00:00"
            )

    # =====================================
    # APPLY VEHICLE SPEED
    # =====================================

    def apply_vehicle_speed(
        self,
        speed_kmh
    ):

        controls = airsim.CarControls()

        throttle = min(
            speed_kmh / 100,
            1.0
        )

        controls.throttle = throttle

        self.client.setCarControls(
            controls
        )

        print()

        print(
            f"Vehicle Speed Applied: "
            f"{speed_kmh} km/h"
        )

    # =====================================
    # APPLY SCENARIO
    # =====================================

    def apply_scenario(
        self,
        scenario
    ):

        print()
        print(
            "===== APPLYING SCENARIO ====="
        )

        # -------------------------
        # WEATHER
        # -------------------------

        self.apply_weather(
            scenario["weather"]
        )

        # -------------------------
        # VEHICLE SPEED
        # -------------------------

        vehicle_speed = (
            scenario["traffic"][
                "average_speed"
            ]
        )

        self.apply_vehicle_speed(
            vehicle_speed
        )

        # -------------------------
        # PEDESTRIAN
        # -------------------------

        pedestrian = (
            scenario["pedestrian"]
        )

        print()
        print(
            "Pedestrian Scenario:"
        )

        print(pedestrian)

        # -------------------------
        # CORNER CASE
        # -------------------------

        corner_case = (
            scenario["corner_case"]
        )

        print()
        print(
            "Corner Case:"
        )

        print(corner_case)

        print()
        print(
            "Scenario Applied Successfully"
        )

    # =====================================
    # SHUTDOWN
    # =====================================

    def shutdown(self):

        controls = airsim.CarControls()

        controls.throttle = 0.0

        controls.brake = 1.0

        self.client.setCarControls(
            controls
        )

        self.client.enableApiControl(
            False
        )

        print()
        print(
            "AirSim Shutdown"
        )