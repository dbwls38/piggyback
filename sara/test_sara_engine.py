from sara_engine import (
    TTCCalculator,
    SaraEngine,
    ControllabilityClassifier
)


def test_controllability_c3():

    c = ControllabilityClassifier()

    assert c.classify(0.5) == "C3"


def test_controllability_c2():

    c = ControllabilityClassifier()

    assert c.classify(2.0) == "C2"


def test_controllability_c1():

    c = ControllabilityClassifier()

    assert c.classify(5.0) == "C1"


def test_full_pipeline_critical():

    distance = 1
    relative_speed = 2

    ttc = TTCCalculator.calculate(
        distance,
        relative_speed
    )

    sara = SaraEngine().assess(ttc)

    controllability = (
        ControllabilityClassifier()
        .classify(ttc)
    )

    assert ttc == 0.5
    assert sara == "CRITICAL"
    assert controllability == "C3"


def test_full_pipeline_dangerous():

    distance = 10
    relative_speed = 5

    ttc = TTCCalculator.calculate(
        distance,
        relative_speed
    )

    sara = SaraEngine().assess(ttc)

    controllability = (
        ControllabilityClassifier()
        .classify(ttc)
    )

    assert ttc == 2.0
    assert sara == "DANGEROUS"
    assert controllability == "C2"


def test_full_pipeline_safe():

    distance = 50
    relative_speed = 10

    ttc = TTCCalculator.calculate(
        distance,
        relative_speed
    )

    sara = SaraEngine().assess(ttc)

    controllability = (
        ControllabilityClassifier()
        .classify(ttc)
    )

    assert ttc == 5.0
    assert sara == "SAFE"
    assert controllability == "C1"