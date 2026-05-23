import random


class VehicleManager:

    def __init__(
        self,
        world
    ):

        self.world = world

        self.vehicle = None

    def spawn_vehicle(self):

        blueprint_library = (
            self.world.get_blueprint_library()
        )

        vehicle_bp = (
            blueprint_library.filter(
                "vehicle.*"
            )[0]
        )

        spawn_points = (
            self.world.get_map()
            .get_spawn_points()
        )

        spawn_point = (
            random.choice(
                spawn_points
            )
        )

        self.vehicle = (
            self.world.spawn_actor(
                vehicle_bp,
                spawn_point
            )
        )

        print()

        print(
            "[VEHICLE SPAWNED]"
        )

        return self.vehicle

    def set_autopilot(
        self,
        enabled=True
    ):

        if self.vehicle:

            self.vehicle.set_autopilot(
                enabled
            )

            print()

            print(
                f"[AUTOPILOT] "
                f"{enabled}"
            )

    def destroy_vehicle(self):

        if self.vehicle:

            self.vehicle.destroy()

            print()

            print(
                "[VEHICLE DESTROYED]"
            )