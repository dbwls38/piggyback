#테스트 완료#
from sara_engine import (
    TTCCalculator,
    SaraEngine,
    RiskQuantifier,
    ControllabilityClassifier
)


def test_controllability_c3():

    risk_score = 85

    c = ControllabilityClassifier()

    result = c.classify(
        ttc=0.5,
        risk_score=risk_score,
        visibility=10
    )

    assert result == "C3"


def test_controllability_c2():

    risk_score = 55

    c = ControllabilityClassifier()

    result = c.classify(
        ttc=2.0,
        risk_score=risk_score,
        visibility=25
    )

    assert result == "C2"


def test_controllability_c1():

    risk_score = 20

    c = ControllabilityClassifier()

    result = c.classify(
        ttc=5.0,
        risk_score=risk_score,
        visibility=100
    )

    assert result == "C1"


def test_full_pipeline_critical():

    distance = 1
    relative_speed = 2
    visibility = 10

    ttc = TTCCalculator.calculate(
        distance,
        relative_speed
    )

    risk_score = (
        RiskQuantifier()
        .quantify(
            ttc,
            visibility
        )
    )

    sara = SaraEngine().assess(ttc)

    controllability = (
        ControllabilityClassifier()
        .classify(
            ttc,
            risk_score,
            visibility
        )
    )

    assert ttc == 0.5
    assert sara == "CRITICAL"
    assert controllability == "C3"


def test_full_pipeline_dangerous():

    distance = 10
    relative_speed = 5
    visibility = 25

    ttc = TTCCalculator.calculate(
        distance,
        relative_speed
    )

    risk_score = (
        RiskQuantifier()
        .quantify(
            ttc,
            visibility
        )
    )

    sara = SaraEngine().assess(ttc)

    controllability = (
        ControllabilityClassifier()
        .classify(
            ttc,
            risk_score,
            visibility
        )
    )

    assert ttc == 2.0
    assert sara == "DANGEROUS"
    assert controllability == "C2"


def test_full_pipeline_safe():

    distance = 50
    relative_speed = 10
    visibility = 100

    ttc = TTCCalculator.calculate(
        distance,
        relative_speed
    )

    risk_score = (
        RiskQuantifier()
        .quantify(
            ttc,
            visibility
        )
    )

    sara = SaraEngine().assess(ttc)

    controllability = (
        ControllabilityClassifier()
        .classify(
            ttc,
            risk_score,
            visibility
        )
    )

    assert ttc == 5.0
    assert sara == "SAFE"
    assert controllability == "C1"