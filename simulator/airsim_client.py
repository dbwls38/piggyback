import airsim

class AirSimClient:
    def __init__(self):
        self.client = airsim.CarClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def get_vehicle_state(self):
        return self.client.getCarState()

    def set_controls(self, throttle, steering, brake=0):
        controls = airsim.CarControls()
        controls.throttle = throttle
        controls.steering = steering
        controls.brake = brake

        self.client.setCarControls(controls)