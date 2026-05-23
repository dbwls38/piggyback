# SARA Autonomous Safety SW

SARA 기반 자율주행 안전성 평가 및 개선 플랫폼

## 실행

```bash
pip install -r requirements.txt
python main.py

---

# main.py

```python
from simulator.carla_client import CarlaConnector
from simulator.vehicle_manager import VehicleManager
from simulator.pedestrian_manager import PedestrianManager

from sara.assess.risk_engine import RiskEngine
from sara.react.emergency_brake import EmergencyBrake

import time


def main():
    connector = CarlaConnector()

    world = connector.get_world()

    vehicle_manager = VehicleManager(world)
    pedestrian_manager = PedestrianManager(world)

    vehicle = vehicle_manager.spawn_vehicle()
    pedestrian = pedestrian_manager.spawn_pedestrian()

    risk_engine = RiskEngine()
    brake_system = EmergencyBrake()

    while True:
        vehicle_location = vehicle.get_location()
        pedestrian_location = pedestrian.get_location()

        risk_data = risk_engine.evaluate(
            vehicle_location,
            pedestrian_location,
            vehicle_velocity=15.0,
            pedestrian_velocity=1.2
        )

        print(risk_data)

        if risk_data["danger"]:
            brake_system.apply(vehicle)

        time.sleep(0.1)


if __name__ == "__main__":
    main()