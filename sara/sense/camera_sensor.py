class CameraSensor:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def capture(self):
        return "camera_frame"