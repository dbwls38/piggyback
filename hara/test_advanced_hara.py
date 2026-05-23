from hara.dynamic_exposure_model import (
    DynamicExposureModel
)

from hara.scenario_risk_graph import (
    ScenarioRiskGraph
)

from hara.safety_goal_generator import (
    SafetyGoalGenerator
)


scenario = {

    "traffic": {

        "vehicle_density":
            48
    },

    "weather": {

        "condition":
            "night_rain"
    },

    "pedestrian": {

        "behavior":
            "sudden_run"
    }
}


sara_result = {

    "ttc":
        1.12,

    "controllability":
        "C3"
}


hara_result = {

    "asil":
        "ASIL-D",

    "controllability":
        "C3"
}


# Dynamic Exposure
exposure_model = (
    DynamicExposureModel()
)

exposure = (
    exposure_model.calculate(
        scenario
    )
)

print()

print(
    f"Dynamic Exposure: {exposure}"
)

# Risk Graph
risk_graph = (
    ScenarioRiskGraph()
)

graph = (
    risk_graph.build_graph(
        scenario,
        sara_result,
        hara_result
    )
)

risk_graph.visualize(
    graph
)


# Safety Goal
goal_generator = (
    SafetyGoalGenerator()
)

goal = (
    goal_generator.generate(
        hara_result
    )
)

print()

print(
    "===== SAFETY GOAL ====="
)

print(goal)