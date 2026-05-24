class VehicleController:

    def __init__(self, client):
        self.client = client

    def emergency_stop(self):

        controls = airsim.CarControls()
        controls.brake = 1.0

        self.client.setCarControls(controls)