from ai_hazard_generator.scenario_generator import (
    ScenarioGenerator
)

from sara.assess.sara_engine import (
    SARAEngine
)

from hara.hara_engine import (
    HARAEngine
)


def test_full_pipeline():

    generator = (
        ScenarioGenerator()
    )

    scenario = (
        generator.generate()
    )

    sara_engine = (
        SARAEngine()
    )

    detected_object = {

        "distance":
            7,

        "relative_speed":
            14
    }

    sara_result = (
        sara_engine.evaluate(
            detected_object,
            visibility=12
        )
    )

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

    print(
        "===== FULL PIPELINE TEST ====="
    )

    print()

    print(
        "Scenario:"
    )

    print(scenario)

    print()

    print(
        "SARA Result:"
    )

    print(sara_result)

    print()

    print(
        "HARA Result:"
    )

    print(hara_result)

    assert (
        hara_result["asil"]
        is not None
    )