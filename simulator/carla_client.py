import carla


class CarlaClient:

    def __init__(
        self,
        host="localhost",
        port=2000
    ):

        self.client = carla.Client(
            host,
            port
        )

        self.client.set_timeout(10.0)

        self.world = (
            self.client.get_world()
        )

        print()

        print(
            "[CONNECTED TO CARLA]"
        )

    def get_world(self):

        return self.world

    def reload_world(self):

        self.client.reload_world()

        print()

        print(
            "[WORLD RELOADED]"
        )