from sara.assess.risk_engine import RiskEngine


class DummyLocation:
    def __init__(self, x, y):
        self.x = x
        self.y = y



def test_risk_engine():
    engine = RiskEngine()

    vehicle_loc = DummyLocation(0, 0)
    pedestrian_loc = DummyLocation(10, 0)

    result = engine.evaluate(
        vehicle_loc,
        pedestrian_loc,
        vehicle_velocity=10,
        pedestrian_velocity=0
    )

    assert "ttc" in result
    assert "danger" in result