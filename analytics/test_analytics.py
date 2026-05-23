from analytics.risk_logger import (
    RiskLogger
)
from analytics.metrics_dashboard import (
    MetricsDashboard
)
from analytics.scenario_recorder import (
    ScenarioRecorder
)
from analytics.statistical_analyzer import (
    StatisticalAnalyzer
)

scenario = {

    "scenario_type":
        "right_turn_pedestrian",

    "weather": {
        "condition":
            "night_rain"
    },

    "corner_case": {
        "type":
            "blind_spot_pedestrian"
    },

    "traffic": {
        "average_speed":
            45
    },

    "pedestrian": {
        "behavior":
            "sudden_run"
    }
}


sara_result = {

    "ttc": 1.24,

    "controllability":
        "C3"
}


hara_result = {

    "severity":
        "S3",

    "exposure":
        "E4",

    "asil":
        "ASIL-D"
}


logger = RiskLogger()

logger.save(
    scenario,
    sara_result,
    hara_result
)


recorder = ScenarioRecorder()

recorder.record(
    scenario
)

dashboard = MetricsDashboard()

dashboard.display(
    sara_result,
    hara_result
)

analyzer = StatisticalAnalyzer()
analyzer.analyze(
    "logs/scenario_logs/scenario_records.csv"
)