#TTC
#Controllability
#Severity
#Exposure
#ASIL
#Safety Goal
#Full Pipeline


from hara.asil_classifier import (
    TTCCalculator,
    ControllabilityClassifier,
    SeverityAnalyzer,
    DynamicExposureModel,
    ASILClassifier,
    SafetyGoalGenerator,
    HARAEngine
)


# -------------------------
# TTC Calculator
# -------------------------
def test_ttc_calculation():

    ttc = TTCCalculator.calculate(
        distance=20,
        relative_speed=10
    )

    assert ttc == 2.0


def test_ttc_infinite():

    ttc = TTCCalculator.calculate(
        distance=20,
        relative_speed=0
    )

    assert ttc == float("inf")


# -------------------------
# Controllability
# -------------------------

def test_controllability_c1():

    result = (
        ControllabilityClassifier()
        .classify(5.0)
    )

    assert result == "C1"


def test_controllability_c2():

    result = (
        ControllabilityClassifier()
        .classify(2.0)
    )

    assert result == "C2"


def test_controllability_c3():

    result = (
        ControllabilityClassifier()
        .classify(0.5)
    )

    assert result == "C3"


# -------------------------
# Severity
# -------------------------

def test_severity_s1():

    scenario = {
        "traffic": {
            "average_speed": 30,
            "vehicle_density": 10
        },
        "weather": {
            "condition": "clear"
        },
        "pedestrian": {
            "behavior": "normal"
        },
        "corner_case": {
            "type": "none"
        }
    }

    result = (
        SeverityAnalyzer()
        .analyze(scenario)
    )

    assert result == "S1"


def test_severity_s2():

    scenario = {
        "traffic": {
            "average_speed": 50,
            "vehicle_density": 10
        },
        "weather": {
            "condition": "clear"
        },
        "pedestrian": {
            "behavior": "normal"
        },
        "corner_case": {
            "type": "none"
        }
    }

    result = (
        SeverityAnalyzer()
        .analyze(scenario)
    )

    assert result == "S2"


def test_severity_s3():

    scenario = {
        "traffic": {
            "average_speed": 70,
            "vehicle_density": 10
        },
        "weather": {
            "condition": "fog"
        },
        "pedestrian": {
            "behavior": "normal"
        },
        "corner_case": {
            "type": "none"
        }
    }

    result = (
        SeverityAnalyzer()
        .analyze(scenario)
    )

    assert result == "S3"


# -------------------------
# Exposure
# -------------------------
def test_exposure_e2():

    scenario = {
        "traffic": {
            "average_speed": 30,
            "vehicle_density": 30
        },
        "weather": {
            "condition": "clear"
        },
        "pedestrian": {
            "behavior": "normal"
        },
        "corner_case": {
            "type": "none"
        }
    }

    result = (
        DynamicExposureModel()
        .calculate(scenario)
    )

    assert result == "E2"


def test_exposure_e4():

    scenario = {
        "traffic": {
            "average_speed": 50,
            "vehicle_density": 50
        },
        "weather": {
            "condition": "fog"
        },
        "pedestrian": {
            "behavior": "jaywalking"
        },
        "corner_case": {
            "type": "none"
        }
    }

    result = (
        DynamicExposureModel()
        .calculate(scenario)
    )

    assert result == "E4"


# -------------------------
# ASIL
# -------------------------

def test_asil_d():

    asil = (
        ASILClassifier()
        .classify(
            "S3",
            "E4",
            "C3"
        )
    )

    assert asil == "ASIL-D"


def test_asil_c():

    asil = (
        ASILClassifier()
        .classify(
            "S3",
            "E4",
            "C2"
        )
    )

    assert asil == "ASIL-C"


def test_asil_b():

    asil = (
        ASILClassifier()
        .classify(
            "S2",
            "E3",
            "C2"
        )
    )

    assert asil == "ASIL-B"


def test_asil_a():

    asil = (
        ASILClassifier()
        .classify(
            "S2",
            "E2",
            "C2"
        )
    )

    assert asil == "ASIL-A"


def test_qm():

    asil = (
        ASILClassifier()
        .classify(
            "S1",
            "E1",
            "C1"
        )
    )

    assert asil == "QM"


# -------------------------
# Safety Goal
# -------------------------

def test_safety_goal_asil_d():

    result = (
        SafetyGoalGenerator()
        .generate(
            {
                "asil": "ASIL-D",
                "controllability": "C3"
            }
        )
    )

    assert (
        result["requirement"]
        ==
        "Emergency braking must activate within 300ms."
    )


# -------------------------
# Full Pipeline
# -------------------------

def test_full_pipeline():

    scenario = {
        "traffic": {
            "average_speed": 70,
            "vehicle_density": 50
        },
        "weather": {
            "condition": "fog"
        },
        "pedestrian": {
            "behavior": "jaywalking"
        },
        "corner_case": {
            "type": "blind_spot_pedestrian"
        }
    }

    result = (
        HARAEngine()
        .evaluate(
            scenario=scenario,
            distance=5,
            relative_speed=10
        )
    )

    assert result["ttc"] == 0.5
    assert result["severity"] == "S3"
    assert result["exposure"] == "E4"
    assert result["controllability"] == "C3"
    assert result["asil"] == "ASIL-D"