class ScenarioLoader:

    def __init__(
        self,
        world
    ):

        self.world = world

    def load_map(
        self,
        town="Town05"
    ):

        print()

        print(
            f"[LOADING MAP] {town}"
        )

    def load_scenario(
        self,
        scenario_name
    ):

        print()

        print(
            f"[SCENARIO] "
            f"{scenario_name}"
        )