import random


class PedestrianManager:
    def __init__(self, world):
        self.world = world
        self.blueprints = world.get_blueprint_library()

    def spawn_pedestrian(self):
        pedestrian_bp = self.blueprints.filter("walker.pedestrian.*")[0]

        spawn_point = random.choice(
            self.world.get_map().get_spawn_points()
        )

        pedestrian = self.world.spawn_actor(pedestrian_bp, spawn_point)

        return pedestrian