from sara.assess.ttc_calculator import TTCCalculator

def test_ttc_calculation():
    calc = TTCCalculator()

    ttc = calc.calculate(10, 5)

    assert ttc == 2