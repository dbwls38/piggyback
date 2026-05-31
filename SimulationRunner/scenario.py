# scenario.py
from dataclasses import dataclass

@dataclass
class Scenario:
    scenario_type: str
    weather: dict
    traffic: dict
    pedestrian: dict
    corner_case: dict