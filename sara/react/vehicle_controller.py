import airsim
class VehicleController:

    def __init__(self, client):

        self.client = client

    def drive_backward(self):

        controls = airsim.CarControls()

        controls.throttle = 0.5

        self.client.setCarControls(
            controls
        )

    def brake(self):

        controls = airsim.CarControls()

        controls.brake = 1.0

        self.client.setCarControls(
            controls
        )
if __name__ == "__main__":
    import time

    from simulator.airsim_client import (
        AirSimClient
    )

    from sara.react.vehicle_controller import (
        VehicleController
    )

    simulator = AirSimClient()

    client = simulator.client

    controller = VehicleController(
        client
    )

    print("START")

    controller.drive_backward()

    time.sleep(5)

    controller.brake()

    print("BRAKE")