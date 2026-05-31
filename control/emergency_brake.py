import airsim
class EmergencyBrake:

    def __init__(self, client):

        self.client = client

    def apply(self):

        controls = airsim.CarControls()

        controls.throttle = 0.0
        controls.brake = 1.0
        controls.steering = 0.0

        self.client.setCarControls(
            controls
        )

        print(
            "EMERGENCY BRAKE ACTIVATED"
        )