# scenario_generator.py

from SimulationRunner.scenario import Scenario
from SimulationRunner.weather import WeatherGenerator
from SimulationRunner.traffic import TrafficGenerator
from SimulationRunner.pedestrian import PedestrianBehaviorAI
from SimulationRunner.corner_case import CornerCaseGenerator

class ScenarioGenerator:

    def __init__(self):
        self.weather = WeatherGenerator()
        self.traffic = TrafficGenerator()
        self.pedestrian = PedestrianBehaviorAI()
        self.corner_case = CornerCaseGenerator()

    def generate(self):

        return Scenario(
            scenario_type="autonomous_driving_test",
            weather=self.weather.generate(),
            traffic=self.traffic.generate(),
            pedestrian=self.pedestrian.generate(),
            corner_case=self.corner_case.generate()
        )