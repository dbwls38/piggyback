import unittest

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

from simulator.airsim_client import (
    CarlaClient
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

        self.client = CarlaClient()

        self.world = (
            self.client.get_world()
        )

        self.loader = (
            ScenarioLoader(
                self.world
            )
        )

        self.vehicle_manager = (
            VehicleManager(
                self.world
            )
        )

        self.pedestrian_manager = (
            PedestrianManager(
                self.world
            )
        )

        self.environment_manager = (
            EnvironmentManager(
                self.world
            )
        )

    def run(self):

        # 맵 로드
        self.loader.load_map(
            "Town05"
        )

        # 날씨 설정
        self.environment_manager.set_night_rain()

        # 차량 생성
        vehicle = (
            self.vehicle_manager.spawn_vehicle()
        )

        self.vehicle_manager.set_autopilot(
            True
        )

        # 보행자 생성
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

    def shutdown(self):

        self.vehicle_manager.destroy_vehicle()

        self.pedestrian_manager.destroy_all()

        print()

        print(
            "[SIMULATION SHUTDOWN]"
        )