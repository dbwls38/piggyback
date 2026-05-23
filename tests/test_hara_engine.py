from hara.hara_engine import (
    HARAEngine
)


def test_hara_engine():

    # 테스트용 시나리오
    scenario = {

        "traffic": {

            "average_speed": 72,

            "vehicle_density": 48
        },

        "weather": {

            "condition": "night_rain"
        },

        "corner_case": {

            "type": "blind_spot_pedestrian"
        }
    }

    # SARA 결과
    sara_result = {

        "controllability": "C3"
    }

    # HARA 엔진 생성
    engine = HARAEngine()

    # HARA 평가
    result = engine.evaluate(
        scenario,
        sara_result
    )

    print()

    print("===== HARA ENGINE TEST =====")

    print()

    print(
        f"Severity: "
        f"{result['severity']}"
    )

    print(
        f"Exposure: "
        f"{result['exposure']}"
    )

    print(
        f"Controllability: "
        f"{result['controllability']}"
    )

    print(
        f"ASIL: "
        f"{result['asil']}"
    )

    # 검증
    assert result["severity"] == "S3"

    assert result["exposure"] == "E4"

    assert (
        result["controllability"]
        == "C3"
    )

    assert result["asil"] == "ASIL-D"