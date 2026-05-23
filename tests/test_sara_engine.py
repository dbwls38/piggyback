from sara.assess.sara_engine import (
    SARAEngine
)


def test_sara_engine():

    engine = SARAEngine()

    detected_object = {

        "distance":
            8,

        "relative_speed":
            12
    }

    result = engine.evaluate(
        detected_object,
        visibility=12
    )

    print()

    print(
        "===== SARA ENGINE TEST ====="
    )

    print(result)

    assert (
        result["controllability"]
        == "C3"
    )