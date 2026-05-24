import airsim


class AirSimClient:

    def __init__(self):

        self.client = airsim.CarClient()

        self.client.confirmConnection()

        self.client.enableApiControl(
            True
        )

        print()

        print(
            "AirSim Connected"
        )