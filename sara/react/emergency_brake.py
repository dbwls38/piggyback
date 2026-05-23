import carla


class EmergencyBrake:
    def apply(self, vehicle):
        control = carla.VehicleControl()
        control.brake = 1.0

        vehicle.apply_control(control)

        print("EMERGENCY BRAKE ACTIVATED")