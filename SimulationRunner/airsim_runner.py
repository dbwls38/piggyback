# airsim_runner.py
import airsim
class AirSimRunner:

    def __init__(self):
        self.client = airsim.CarClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

        self.running = False


        print("[AirSim] Connected")

    # -------------------------
    # WEATHER
    # -------------------------
    def apply_weather(self, weather):

        self.client.simEnableWeather(True)

        condition = weather["condition"]

        print(f"[WEATHER] {condition}")

        if condition == "clear":
            self._clear()

        elif condition in ["rain", "heavy_rain"]:
            self._rain()

        elif condition == "fog":
            self._fog()

        elif condition == "night":
            self.client.simSetTimeOfDay(True, "2025-01-01 22:00:00")

    def _clear(self):
        self.client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.0)
        self.client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.0)

    def _rain(self):
        self.client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.8)
        self.client.simSetWeatherParameter(airsim.WeatherParameter.Roadwetness, 0.7)

    def _fog(self):
        self.client.simSetWeatherParameter(airsim.WeatherParameter.Fog, 0.7)

    # -------------------------
    # TRAFFIC
    # -------------------------
    def apply_traffic(self, traffic):

        speed = traffic["average_speed"]
        self.apply_speed(speed)

        print(f"[TRAFFIC] pattern={traffic['pattern']}")

    # -------------------------
    # SPEED CONTROL
    # -------------------------
    def apply_speed(self, speed_kmh):

        controls = airsim.CarControls()
        controls.throttle = min(speed_kmh / 100, 1.0)

        self.client.setCarControls(controls)

        print(f"[SPEED] {speed_kmh} km/h")

    # -------------------------
    # PEDESTRIAN (LOG ONLY)
    # -------------------------
    def apply_pedestrian(self, pedestrian):
        print("[PEDESTRIAN]")
        print(pedestrian)

    # -------------------------
    # CORNER CASE (LOG ONLY)
    # -------------------------
    def apply_corner_case(self, corner_case):
        print("[CORNER CASE]")
        print(corner_case)

    # -------------------------
    # MAIN ENTRY
    # -------------------------
    def apply_scenario(self, scenario):

        print("\n===== APPLY SCENARIO =====")

        self.apply_weather(scenario["weather"])
        self.apply_traffic(scenario["traffic"])
        self.apply_pedestrian(scenario["pedestrian"])
        self.apply_corner_case(scenario["corner_case"])

        print("\n===== DONE =====")

    # -------------------------
    # SHUTDOWN
    # -------------------------
    def shutdown(self):

        controls = airsim.CarControls()
        controls.throttle = 0
        controls.brake = 1

        self.client.setCarControls(controls)
        self.client.enableApiControl(False)

        print("[AirSim] Shutdown")