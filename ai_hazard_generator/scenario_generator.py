from ai_hazard_generator.weather_generator import (
    WeatherGenerator
)
from ai_hazard_generator.pedestrian_behavior_ai import (
    PedestrianBehaviorAI
)
from ai_hazard_generator.traffic_pattern_generator import (
    TrafficPatternGenerator
)
from ai_hazard_generator.corner_case_generator import (
    CornerCaseGenerator
)

class ScenarioGenerator:

    def __init__(self):

        self.weather_generator = (
            WeatherGenerator()
        )

        self.pedestrian_ai = (
            PedestrianBehaviorAI()
        )

        self.traffic_generator = (
            TrafficPatternGenerator()
        )

        self.corner_case_generator = (
            CornerCaseGenerator()
        )

    def generate(self):

        weather = (
            self.weather_generator.generate()
        )

        pedestrian_behavior = (
            self.pedestrian_ai.generate()
        )

        traffic_pattern = (
            self.traffic_generator.generate()
        )

        corner_case = (
            self.corner_case_generator.generate()
        )

        scenario = {

            "scenario_type":
                "right_turn_pedestrian",

            "weather":
                weather,

            "pedestrian":
                pedestrian_behavior,

            "traffic":
                traffic_pattern,

            "corner_case":
                corner_case
        }

        return scenario