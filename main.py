from simulator.simulation_runner import (
    SimulationRunner
)

from ai_hazard_generator.scenario_generator import (
    ScenarioGenerator
)

from sara.sense.radar_sensor import (
    RadarSensor
)

from sara.sense.object_detector import (
    ObjectDetector
)

from sara.assess.sara_engine import (
    SARAEngine
)

from sara.react.vehicle_controller import (
    VehicleController
)

from hara.hara_engine import (
    HARAEngine
)

from hara.safety_goal_generator import (
    SafetyGoalGenerator
)

from hara.scenario_risk_graph import (
    ScenarioRiskGraph
)

from analytics.risk_logger import (
    RiskLogger
)

from analytics.metrics_dashboard import (
    MetricsDashboard
)

from analytics.scenario_recorder import (
    ScenarioRecorder
)


def main():

    print()
    print("====================================")
    print(" SARA-HARA SAFETY VALIDATION SYSTEM ")
    print("====================================")

    # =========================
    # SIMULATOR INITIALIZATION
    # =========================

    simulator = SimulationRunner()

    simulation_result = simulator.run()

    # =========================
    # AI HAZARD GENERATION
    # =========================

    scenario_generator = (
        ScenarioGenerator()
    )

    scenario = (
        scenario_generator.generate()
    )

    print()
    print("===== GENERATED SCENARIO =====")
    print(scenario)

    # =========================
    # SENSOR SYSTEM
    # =========================

    radar_sensor = (
        RadarSensor()
    )

    object_detector = (
        ObjectDetector()
    )

    radar_objects = (
        radar_sensor.scan()
    )

    detected_objects = (
        object_detector.detect(
            radar_objects
        )
    )

    print()
    print("===== DETECTED OBJECTS =====")
    print(detected_objects)

    # =========================
    # SARA ENGINE
    # =========================

    sara_engine = (
        SARAEngine()
    )

    controller = (
        VehicleController()
    )

    visibility = (
        scenario["weather"][
            "visibility_distance"
        ]
    )

    sara_results = []

    for obj in detected_objects:

        sara_result = (
            sara_engine.evaluate(
                obj,
                visibility
            )
        )

        sara_results.append(
            sara_result
        )

        print()
        print("===== SARA RESULT =====")
        print(sara_result)

        vehicle = {
            "speed": 72
        }

        controller.react(
            sara_result,
            vehicle
        )

    # 가장 위험한 객체 선택
    sara_result = max(
        sara_results,
        key=lambda x:
        x["risk_score"]
    )

    # =========================
    # HARA ENGINE
    # =========================

    hara_engine = (
        HARAEngine()
    )

    hara_result = (
        hara_engine.evaluate(
            scenario,
            sara_result
        )
    )

    print()
    print("===== HARA RESULT =====")
    print(hara_result)

    # =========================
    # SAFETY GOAL
    # =========================

    safety_goal_generator = (
        SafetyGoalGenerator()
    )

    safety_goal = (
        safety_goal_generator.generate(
            hara_result
        )
    )

    print()
    print("===== SAFETY GOAL =====")
    print(safety_goal)

    # =========================
    # RISK GRAPH
    # =========================

    risk_graph_engine = (
        ScenarioRiskGraph()
    )

    risk_graph = (
        risk_graph_engine.build_graph(
            scenario,
            sara_result,
            hara_result
        )
    )

    risk_graph_engine.visualize(
        risk_graph
    )

    # =========================
    # ANALYTICS
    # =========================

    logger = (
        RiskLogger()
    )

    logger.save(
        scenario,
        sara_result,
        hara_result
    )

    recorder = (
        ScenarioRecorder()
    )

    recorder.record(
        scenario
    )

    dashboard = (
        MetricsDashboard()
    )

    dashboard.display(
        sara_result,
        hara_result
    )

    # =========================
    # FINAL RESULT
    # =========================

    print()
    print("================================")
    print(" FINAL SAFETY VALIDATION RESULT ")
    print("================================")

    print()

    print(
        f"Scenario: "
        f"{scenario['scenario_type']}"
    )

    print(
        f"TTC: "
        f"{sara_result['ttc']}"
    )

    print(
        f"Risk Level: "
        f"{sara_result['risk_level']}"
    )

    print(
        f"Controllability: "
        f"{hara_result['controllability']}"
    )

    print(
        f"ASIL: "
        f"{hara_result['asil']}"
    )

    print()

    print("================================")

    # =========================
    # SHUTDOWN
    # =========================

    input(
        "\nPress Enter to shutdown..."
    )

    simulator.shutdown()


if __name__ == "__main__":

    main()