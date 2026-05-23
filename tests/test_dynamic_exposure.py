from hara.dynamic_exposure_model import (
    DynamicExposureModel
)


def test_dynamic_exposure():

    model = (
        DynamicExposureModel()
    )

    scenario = {

        "traffic": {

            "vehicle_density":
                45
        },

        "weather": {

            "condition":
                "night_rain"
        },

        "pedestrian": {

            "behavior":
                "sudden_run"
        }
    }

    exposure = model.calculate(
        scenario
    )

    print()

    print(
        "===== DYNAMIC EXPOSURE TEST ====="
    )

    print(
        f"Exposure: "
        f"{exposure}"
    )

    assert exposure == "E4"