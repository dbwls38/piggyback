from scenarios.right_turn_pedestrian import (
    RightTurnPedestrianScenario
)

from scenarios.jaywalking import (
    JaywalkingScenario
)

from scenarios.sudden_cut_in import (
    SuddenCutInScenario
)

from scenarios.night_rain import (
    NightRainScenario
)

from scenarios.sensor_failure import (
    SensorFailureScenario
)


class ScenarioRunner:

    def __init__(self):

        self.scenarios = [

            RightTurnPedestrianScenario(),

            JaywalkingScenario(),

            SuddenCutInScenario(),

            NightRainScenario(),

            SensorFailureScenario()
        ]

    def run_all(self):

        for scenario in self.scenarios:

            scenario.spawn()

            result = scenario.run()

            print()

            print(result)

from scenarios.scenario_runner import (
    ScenarioRunner
)


runner = ScenarioRunner()

runner.run_all()