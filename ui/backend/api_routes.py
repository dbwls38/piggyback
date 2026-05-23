from flask import (
    Blueprint,
    jsonify,
    request
)

from ai_hazard_generator.scenario_generator import (
    ScenarioGenerator
)

from sara.assess.sara_engine import (
    SARAEngine
)

from hara.hara_engine import (
    HARAEngine
)

from analytics.risk_logger import (
    RiskLogger
)


api = Blueprint(
    "api",
    __name__
)


@api.route(
    "/health",
    methods=["GET"]
)
def health_check():

    return jsonify({

        "status":
            "OK",

        "service":
            "SARA-HARA Safety Platform"
    })


@api.route(
    "/generate_scenario",
    methods=["GET"]
)
def generate_scenario():

    generator = (
        ScenarioGenerator()
    )

    scenario = (
        generator.generate()
    )

    return jsonify(
        scenario
    )


@api.route(
    "/run_hara",
    methods=["POST"]
)
def run_hara():

    data = request.json

    scenario = data["scenario"]

    detected_object = {

        "distance":
            data.get(
                "distance",
                8
            ),

        "relative_speed":
            data.get(
                "relative_speed",
                12
            )
    }

    visibility = data.get(
        "visibility",
        15
    )

    # SARA
    sara_engine = (
        SARAEngine()
    )

    sara_result = (
        sara_engine.evaluate(
            detected_object,
            visibility
        )
    )

    # HARA
    hara_engine = (
        HARAEngine()
    )

    hara_result = (
        hara_engine.evaluate(
            scenario,
            sara_result
        )
    )

    # 로그 저장
    logger = (
        RiskLogger()
    )

    logger.save(
        scenario,
        sara_result,
        hara_result
    )

    return jsonify({

        "scenario":
            scenario,

        "sara_result":
            sara_result,

        "hara_result":
            hara_result
    })