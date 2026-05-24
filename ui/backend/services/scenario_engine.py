class ScenarioEngine:

    def generate(self, scenario_type):

        if scenario_type == "right_turn_pedestrian":
            return {
                "vehicle_speed": 30,
                "pedestrian": True,
                "weather": "clear"
            }

        if scenario_type == "straight":
            return {
                "vehicle_speed": 50,
                "pedestrian": False,
                "weather": "rain"
            }