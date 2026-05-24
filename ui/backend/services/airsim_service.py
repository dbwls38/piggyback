import airsim

class AirSimService:

    def __init__(self):
        self.client = airsim.CarClient()
        self.connected = False

    def connect(self):
        self.client.confirmConnection()
        self.connected = True

    def start(self):
        self.client.setCarControls(
            airsim.CarControls(throttle=0.5)
        )

    def stop(self):
        self.client.setCarControls(
            airsim.CarControls(throttle=0)
        )