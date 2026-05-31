from SimulationRunner.airsim_runner import AirSimRunner
from ai_hazard_generator.scenario_generator import ScenarioGenerator

from TestSensor.radar_sensor import RadarSensor
from TestSensor.camera_sensor import CameraSensor
from TestSensor.lidar_sensor import LidarSensor
from TestSensor.object_detector import ObjectDetector

from sara.sara_engine import SaraEngine
from control.vehicle_controller import VehicleController

from hara.asil_classifier import HARAEngine, SafetyGoalGenerator

from analytics.risk_logger import RiskLogger
from analytics.metrics_dashboard import MetricsDashboard
from analytics.scenario_recorder import ScenarioRecorder


def main():

    print("\n===== AIRSIM SAFETY SIMULATION START =====\n")

    # ===================================
    # INIT
    # ===================================

    runner = AirSimRunner()
    client = runner.client   # ✅ 핵심: simulator 제거

    print("\n===== AIRSIM CONNECTED =====")

    # ===================================
    # SCENARIO
    # ===================================

    scenario = ScenarioGenerator().generate()

    print("\n===== GENERATED SCENARIO =====")
    print(scenario)

    # ===================================
    # APPLY SCENARIO
    # ===================================

    runner.apply_scenario(scenario)

    runner.run()

    # ===================================
    # SENSOR
    # ===================================

    radar_sensor = RadarSensor(client)
    camera_sensor = CameraSensor(client)
    lidar_sensor = LidarSensor(client)
    object_detector = ObjectDetector()

    radar_objects = radar_sensor.scan()
    camera_frame = camera_sensor.capture()
    lidar_points = lidar_sensor.get_point_cloud()

    detected_objects = object_detector.detect(
        radar_objects,
        camera_frame,
        lidar_points
    )

    print("\n===== DETECTED OBJECTS =====")
    print(detected_objects)

    # ===================================
    # SARA
    # ===================================

    sara_engine = SaraEngine()
    controller = VehicleController(client)

    visibility = scenario["weather"]["visibility_distance"]

    sara_results = []

    for obj in detected_objects:

        result = sara_engine.evaluate(obj, visibility)
        sara_results.append(result)

        vehicle_state = runner.get_vehicle_state()
        controller.react(result, vehicle_state)

    # ===================================
    # MOST DANGEROUS
    # ===================================

    most_risky = max(sara_results, key=lambda x: x["risk_score"])

    # ===================================
    # HARA
    # ===================================

    hara_engine = HARAEngine()

    hara_result = hara_engine.evaluate(
        scenario,
        most_risky
    )

    print("\n===== HARA RESULT =====")
    print(hara_result)

    # ===================================
    # SAFETY GOAL
    # ===================================

    safety_goal = SafetyGoalGenerator().generate(hara_result)

    print("\n===== SAFETY GOAL =====")
    print(safety_goal)

    # ===================================
    # LOGGING
    # ===================================

    RiskLogger().save(scenario, most_risky, hara_result)
    ScenarioRecorder().record(scenario)
    MetricsDashboard().display(most_risky, hara_result)

    # ===================================
    # SHUTDOWN
    # ===================================

    input("\nPress Enter to shutdown...")
    runner.shutdown()


if __name__ == "__main__":
    main()