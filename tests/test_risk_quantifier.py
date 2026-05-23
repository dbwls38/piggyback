from sara.assess.risk_quantifier import (
    RiskQuantifier
)


def test_risk_quantifier():

    quantifier = (
        RiskQuantifier()
    )

    risk_score = (
        quantifier.quantify(
            ttc=1.2,
            collision_probability=0.9,
            visibility=15
        )
    )

    print()

    print(
        "===== RISK SCORE TEST ====="
    )

    print(
        f"Risk Score: "
        f"{risk_score}"
    )

    assert risk_score > 50