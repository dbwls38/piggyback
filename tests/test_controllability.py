from sara.assess.controllability_estimator import (
    ControllabilityEstimator
)


def test_controllability():

    estimator = (
        ControllabilityEstimator()
    )

    controllability = (
        estimator.estimate(
            ttc=0.9,
            risk_score=92,
            visibility=10
        )
    )

    print()

    print(
        "===== CONTROLLABILITY TEST ====="
    )

    print(
        f"Controllability: "
        f"{controllability}"
    )

    assert controllability == "C3"