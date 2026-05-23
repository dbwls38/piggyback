from sara.react.emergency_brake import (
    EmergencyBrake
)

from sara.react.evasive_steering import (
    EvasiveSteering
)


class VehicleController:

    def __init__(self):

        self.brake = (
            EmergencyBrake()
        )

        self.steering = (
            EvasiveSteering()
        )

    def react(
        self,
        sara_result,
        vehicle
    ):

        controllability = (
            sara_result[
                "controllability"
            ]
        )

        if controllability == "C3":

            self.brake.activate(
                vehicle
            )

            self.steering.avoid()

        elif controllability == "C2":

            self.brake.activate(
                vehicle
            )

        else:

            print(
                "[SAFE DRIVING]"
            )