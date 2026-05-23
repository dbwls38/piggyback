from simulator.simulation_runner import (
    SimulationRunner
)


def test_simulator():

    runner = (
        SimulationRunner()
    )

    result = runner.run()

    print()

    print(
        "===== SIMULATOR TEST ====="
    )

    print(result)

    runner.shutdown()

    assert result is not None