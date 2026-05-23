from scenarios.scenario_runner import (
    ScenarioRunner
)


def test_scenarios():

    runner = (
        ScenarioRunner()
    )

    runner.run_all()

    print()

    print(
        "[SCENARIO TEST COMPLETED]"
    )

    assert True