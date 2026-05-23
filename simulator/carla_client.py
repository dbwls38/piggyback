import carla
from config.settings import CARLA_HOST, CARLA_PORT


class CarlaConnector:
    def __init__(self):
        self.client = carla.Client(CARLA_HOST, CARLA_PORT)
        self.client.set_timeout(10.0)

    def get_world(self):
        return self.client.get_world()