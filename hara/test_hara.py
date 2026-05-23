from hara.hara_engine import (
    HARAEngine
)


scenario = {

    "traffic": {

        "average_speed":
            72,

        "vehicle_density":
            48
    },

    "weather": {

        "condition":
            "night_rain"
    },

    "corner_case": {

        "type":
            "blind_spot_pedestrian"
    }
}


sara_result = {

    "controllability":
        "C3"
}


engine = HARAEngine()

result = engine.evaluate(
    scenario,
    sara_result
)

print()

print("===== HARA RESULT =====")

print(result)