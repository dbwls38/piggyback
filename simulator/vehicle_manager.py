import random


class VehicleManager:
    def __init__(self, world):
        self.world = world
        self.blueprints = world.get_blueprint_library()

    def spawn_vehicle(self):
        vehicle_bp = self.blueprints.filter("vehicle.*")[0]

        spawn_point = random.choice(
            self.world.get_map().get_spawn_points()
        )

        vehicle = self.world.spawn_actor(vehicle_bp, spawn_point)

        return vehicle