from SimulationRunner.airsim_runner import AirSimRunner
from ai_hazard_generator.scenario_generator import ScenarioGenerator

from TestSensor.radar_sensor import RadarSensor
from TestSensor.object_detector import ObjectDetector

from sara.sara_engine import SaraEngine
from sara.sara_engine import RiskQuantifier
from sara.sara_engine import TTCCalculator
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
    client = runner.client

    print("\n===== AIRSIM CONNECTED =====")

    # ===================================
    # SCENARIO
    # ===================================

    scenario = ScenarioGenerator().generate()

    # 🌧️ 강제 RAIN
    scenario["weather"]["condition"] = "rain"
    scenario["weather"]["visibility_distance"] = 40

    print("\n===== GENERATED SCENARIO =====")
    print(scenario)

    # ===================================
    # APPLY SCENARIO
    # ===================================

    runner.apply_scenario(scenario)

    print("\n===== SCENARIO APPLIED =====")

    # ===================================
    # SENSOR (RADAR ONLY)
    # ===================================

    radar_sensor = RadarSensor(client)
    object_detector = ObjectDetector()

    radar_objects = radar_sensor.scan()

    detected_objects = object_detector.detect(radar_objects)

    print("\n===== DETECTED OBJECTS =====")
    print(detected_objects)

    # ===================================
    # SARA
    # ===================================

    print("\n===== SARA START =====")

    sara_engine = SaraEngine()
    controller = VehicleController(client)

    visibility = scenario["weather"]["visibility_distance"]

    sara_results = []

    if not detected_objects:
        print("[WARN] No detected objects")
    else:

        for obj in detected_objects:
            print(f"\n[OBJ] {obj}")

            # ==============================
            # 1. OBJ → TTC 입력 변환
            # ==============================

            distance = obj.get("distance", 20.0)
            rel_speed = obj.get("relative_speed", 5.0)

            ttc = TTCCalculator.calculate(distance, rel_speed)

            print(f"[TTC] {ttc}")

            # ==============================
            # 2. SARA 평가 (핵심 변경)
            # ==============================

            level = sara_engine.assess(ttc)

            # ==============================
            # 3. Risk 계산
            # ==============================

            risk = RiskQuantifier().quantify(ttc, visibility)

            result = {
                "object": obj,
                "ttc": ttc,
                "risk_score": risk,
                "level": level
            }

            print(f"[SARA RESULT] {result}")

            sara_results.append(result)

            # ==============================
            # 4. Control
            # ==============================

            vehicle_state = client.getCarState()
            controller.react(result, vehicle_state)

    print("\n===== SARA END =====")

    # ===================================
    # MOST DANGEROUS
    # ===================================

    most_risky_raw = max(sara_results, key=lambda x: x["risk_score"])

    # ===============================
    # 🔥 ENGINE ADAPTER (핵심)
    # ===============================

    hara_input = {
        "ttc": most_risky_raw["ttc"],
        "risk_score": most_risky_raw["risk_score"],
        "controllability": most_risky_raw["level"]  # SAFE → C1/C2/C3로 가정
    }

    print("\n===== HARA INPUT (ADAPTED) =====")
    print(hara_input)

    # ===================================
    # HARA
    # ===================================

    hara_engine = HARAEngine()

    hara_result = hara_engine.evaluate(
        scenario,
        hara_input
    )

    print("\n===== HARA RESULT =====")
    print(hara_result)

    print("\n===== HARA END =====")

    # ===================================
    # SAFETY GOAL
    # ===================================

    print("\n===== SAFETY GOAL =====")

    safety_goal = SafetyGoalGenerator().generate(hara_result)

    print(safety_goal)

    # ===================================
    # LOGGING
    # ===================================

    print("\n===== LOGGING START =====")

    RiskLogger().save(scenario, hara_result["most_dangerous"], hara_result)

    ScenarioRecorder().record(scenario)

    MetricsDashboard().display(
        hara_result["most_dangerous"],
        hara_result
    )

    print("\n===== LOGGING END =====")

    # ===================================
    # SHUTDOWN
    # ===================================

    input("\nPress Enter to shutdown...")
    runner.shutdown()

    print("\n===== SHUTDOWN COMPLETE =====")


if __name__ == "__main__":
    main()