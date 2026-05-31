from Testscenarios.right_turn_pedestrian import (
    RightTurnPedestrianScenario
)

from Testscenarios.sudden_cutin import (
    SuddenCutInScenario
)

from Testscenarios.night_rain import (
    NightRainScenario
)

from Testscenarios.sensor_failure import (
    SensorFailureScenario
)


class ScenarioRunner:

    def __init__(self):

        self.scenarios = [

            RightTurnPedestrianScenario(),

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


from Testscenarios.scenario_runner import (
    ScenarioRunner
)

runner = ScenarioRunner()

runner.run_all()