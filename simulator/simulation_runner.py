from simulator.airsim_client import (
    AirSimClient
)

from simulator.scenario_loader import (
    ScenarioLoader
)

from simulator.vehicle_manager import (
    VehicleManager
)

from simulator.pedestrian_manager import (
    PedestrianManager
)

from simulator.environment_manager import (
    EnvironmentManager
)


class SimulationRunner:

    def __init__(self):

        # =====================================
        # AIRSIM CLIENT
        # =====================================

        self.simulator = (
            AirSimClient()
        )



        self.client = (
            self.simulator.client
        )

        # =====================================
        # MANAGERS
        # =====================================

        self.loader = (
            ScenarioLoader(
                self.client
            )
        )

        self.vehicle_manager = (
            VehicleManager(
                self.client
            )
        )

        self.vehicle_manager.run_demo()

        self.pedestrian_manager = (
            PedestrianManager(
                self.client
            )
        )

        self.environment_manager = (
            EnvironmentManager(
                self.client
            )
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

        # =====================================
        # WEATHER
        # =====================================

        weather = (
            scenario["weather"]
        )

        condition = (
            weather["condition"]
        )

        if condition == "clear":

            self.environment_manager.set_clear_weather()

        elif condition == "rain":

            self.environment_manager.set_rain_weather()

        elif condition == "night_rain":

            self.environment_manager.set_night_rain()

        elif condition == "fog":

            self.environment_manager.set_fog_weather()

        # =====================================
        # VEHICLE SPEED
        # =====================================

        traffic = (
            scenario["traffic"]
        )

        speed = (
            traffic["average_speed"]
        )

        self.vehicle_manager.set_speed(
            speed
        )

        # =====================================
        # PEDESTRIAN
        # =====================================

        pedestrian = (
            scenario["pedestrian"]
        )

        self.pedestrian_manager.apply_behavior(
            pedestrian
        )

        # =====================================
        # CORNER CASE
        # =====================================

        corner_case = (
            scenario["corner_case"]
        )

        self.handle_corner_case(
            corner_case
        )

        print()
        print(
            "[SCENARIO APPLIED]"
        )

    # =====================================
    # HANDLE CORNER CASE
    # =====================================

    def handle_corner_case(
        self,
        corner_case
    ):

        case_type = (
            corner_case["type"]
        )

        print()

        print(
            "[CORNER CASE]"
        )

        print(case_type)

        if case_type == (
            "sudden_vehicle_cutin"
        ):

            print(
                "Simulating cut-in event"
            )

        elif case_type == (
            "sensor_failure"
        ):

            print(
                "Sensor failure injected"
            )

        elif case_type == (
            "pedestrian_occlusion"
        ):

            print(
                "Pedestrian occlusion detected"
            )

    # =====================================
    # RUN SIMULATION
    # =====================================

    def run(self):

        print()

        print(
            "[AIRSIM SIMULATION START]"
        )

        # =====================================
        # MAP LOAD
        # =====================================

        self.loader.load_map(
            "Blocks"
        )

        # =====================================
        # VEHICLE CONTROL
        # =====================================

        vehicle = (
            self.vehicle_manager.spawn_vehicle()
        )

        self.vehicle_manager.enable_api_control()

        self.vehicle_manager.drive_forward()

        # =====================================
        # PEDESTRIAN
        # =====================================

        pedestrian = (
            self.pedestrian_manager.spawn_pedestrian()
        )

        print()

        print(
            "[SIMULATION RUNNING]"
        )

        return {

            "vehicle":
                vehicle,

            "pedestrian":
                pedestrian
        }

    # =====================================
    # SHUTDOWN
    # =====================================

    def shutdown(self):

        self.vehicle_manager.stop_vehicle()

        self.vehicle_manager.disable_api_control()

        self.pedestrian_manager.destroy_all()

        print()

        print(
            "[SIMULATION SHUTDOWN]"
        )
