import airsim
class VehicleController:

    def __init__(self, client):
        self.client = client

    def react(self, result, vehicle_state):

        risk = result["risk_score"]
        level = result["level"]

        if level == "CRITICAL":
            control = airsim.CarControls()
            control.throttle = 0
            control.brake = 1

        elif level == "DANGEROUS":
            control = airsim.CarControls()
            control.throttle = 0.2
            control.brake = 0.5

        else:
            control = airsim.CarControls()
            control.throttle = 0.6
            control.brake = 0

        self.client.setCarControls(control)
