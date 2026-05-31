#함수 호출 테스트 완료#
import pytest
from unittest.mock import MagicMock, patch
from ai_hazard_generator.scenario_generator import ScenarioGenerator
# =====================================================
# 샘플 데이터
# =====================================================

FAKE_WEATHER = {
    "condition": "rain",
    "visibility_distance": 40,
    "road_friction": 0.55
}

FAKE_PEDESTRIAN = {
    "behavior": "jaywalking",
    "speed": 1.20,
    "visibility": "low"
}

FAKE_TRAFFIC = {
    "pattern": "heavy",
    "vehicle_density": 45,
    "average_speed": 30
}

FAKE_CORNER_CASE = {
    "type": "pedestrian_occlusion",
    "risk_level": "HIGH"
}


# =====================================================
# FIXTURES
# =====================================================

@pytest.fixture
def gen():
    """각 하위 generator 를 MagicMock 으로 교체한 ScenarioGenerator"""
    sg = ScenarioGenerator()
    sg.weather_generator     = MagicMock()
    sg.pedestrian_ai         = MagicMock()
    sg.traffic_generator     = MagicMock()
    sg.corner_case_generator = MagicMock()

    sg.weather_generator.generate.return_value     = FAKE_WEATHER
    sg.pedestrian_ai.generate.return_value         = FAKE_PEDESTRIAN
    sg.traffic_generator.generate.return_value     = FAKE_TRAFFIC
    sg.corner_case_generator.generate.return_value = FAKE_CORNER_CASE

    return sg


@pytest.fixture
def result(gen):
    """generate() 호출 결과를 캐싱"""
    return gen.generate()


# =====================================================
# __init__ : 하위 generator 초기화
# =====================================================

class TestInit:

    def test_weather_generator_created(self):
        """__init__ 시 WeatherGenerator 인스턴스가 생성되어야 한다."""
        with patch("ai_hazard_generator.scenario_generator.WeatherGenerator") as MockW:
            ScenarioGenerator()
            MockW.assert_called_once()
            print(f"\n[PASS] WeatherGenerator() 호출 확인")

    def test_pedestrian_ai_created(self):
        """__init__ 시 PedestrianBehaviorAI 인스턴스가 생성되어야 한다."""
        with patch("ai_hazard_generator.scenario_generator.PedestrianBehaviorAI") as MockP:
            ScenarioGenerator()
            MockP.assert_called_once()
            print(f"\n[PASS] PedestrianBehaviorAI() 호출 확인")

    def test_traffic_generator_created(self):
        """__init__ 시 TrafficPatternGenerator 인스턴스가 생성되어야 한다."""
        with patch("ai_hazard_generator.scenario_generator.TrafficPatternGenerator") as MockT:
            ScenarioGenerator()
            MockT.assert_called_once()
            print(f"\n[PASS] TrafficPatternGenerator() 호출 확인")

    def test_corner_case_generator_created(self):
        """__init__ 시 CornerCaseGenerator 인스턴스가 생성되어야 한다."""
        with patch("ai_hazard_generator.scenario_generator.CornerCaseGenerator") as MockC:
            ScenarioGenerator()
            MockC.assert_called_once()
            print(f"\n[PASS] CornerCaseGenerator() 호출 확인")


# =====================================================
# generate() : 하위 generator 호출 여부
# =====================================================

class TestSubGeneratorCalled:

    def test_weather_generate_called(self, gen):
        """generate() 호출 시 weather_generator.generate() 가 실행되어야 한다."""
        gen.generate()
        gen.weather_generator.generate.assert_called_once()
        print(f"\n[PASS] weather_generator.generate() 호출 확인")

    def test_pedestrian_generate_called(self, gen):
        """generate() 호출 시 pedestrian_ai.generate() 가 실행되어야 한다."""
        gen.generate()
        gen.pedestrian_ai.generate.assert_called_once()
        print(f"\n[PASS] pedestrian_ai.generate() 호출 확인")

    def test_traffic_generate_called(self, gen):
        """generate() 호출 시 traffic_generator.generate() 가 실행되어야 한다."""
        gen.generate()
        gen.traffic_generator.generate.assert_called_once()
        print(f"\n[PASS] traffic_generator.generate() 호출 확인")

    def test_corner_case_generate_called(self, gen):
        """generate() 호출 시 corner_case_generator.generate() 가 실행되어야 한다."""
        gen.generate()
        gen.corner_case_generator.generate.assert_called_once()
        print(f"\n[PASS] corner_case_generator.generate() 호출 확인")

    def test_all_sub_generators_called_exactly_once(self, gen):
        """generate() 1회 호출 시 하위 generator 4개가 각각 정확히 1번씩 호출되어야 한다."""
        gen.generate()
        assert gen.weather_generator.generate.call_count     == 1
        assert gen.pedestrian_ai.generate.call_count         == 1
        assert gen.traffic_generator.generate.call_count     == 1
        assert gen.corner_case_generator.generate.call_count == 1
        print(f"\n[PASS] 4개 하위 generator 모두 1회 호출 확인")


# =====================================================
# generate() : 반환값 구조
# =====================================================

class TestReturnStructure:

    def test_returns_dict(self, result):
        """generate() 는 dict 를 반환해야 한다."""
        assert isinstance(result, dict)
        print(f"\n[PASS] 반환 타입: {type(result).__name__}")

    def test_has_scenario_type_key(self, result):
        """반환값에 'scenario_type' 키가 있어야 한다."""
        assert "scenario_type" in result
        print(f"\n[PASS] 'scenario_type' 키 존재 → 값: {result['scenario_type']}")

    def test_has_weather_key(self, result):
        """반환값에 'weather' 키가 있어야 한다."""
        assert "weather" in result
        print(f"\n[PASS] 'weather' 키 존재 → 값: {result['weather']}")

    def test_has_pedestrian_key(self, result):
        """반환값에 'pedestrian' 키가 있어야 한다."""
        assert "pedestrian" in result
        print(f"\n[PASS] 'pedestrian' 키 존재 → 값: {result['pedestrian']}")

    def test_has_traffic_key(self, result):
        """반환값에 'traffic' 키가 있어야 한다."""
        assert "traffic" in result
        print(f"\n[PASS] 'traffic' 키 존재 → 값: {result['traffic']}")

    def test_has_corner_case_key(self, result):
        """반환값에 'corner_case' 키가 있어야 한다."""
        assert "corner_case" in result
        print(f"\n[PASS] 'corner_case' 키 존재 → 값: {result['corner_case']}")

    def test_no_extra_keys(self, result):
        """5개 키 외 불필요한 키가 없어야 한다."""
        assert set(result.keys()) == {
            "scenario_type", "weather", "pedestrian", "traffic", "corner_case"
        }
        print(f"\n[PASS] 키 목록: {set(result.keys())}")


# =====================================================
# generate() : 반환값 내용
# =====================================================

class TestReturnValues:

    def test_scenario_type_is_right_turn_pedestrian(self, result):
        """scenario_type 은 항상 'right_turn_pedestrian' 이어야 한다."""
        assert result["scenario_type"] == "right_turn_pedestrian"
        print(f"\n[PASS] scenario_type = '{result['scenario_type']}'")

    def test_weather_comes_from_weather_generator(self, result):
        """weather 는 weather_generator.generate() 의 반환값이어야 한다."""
        assert result["weather"] == FAKE_WEATHER
        print(f"\n[PASS] weather = {result['weather']}")

    def test_pedestrian_comes_from_pedestrian_ai(self, result):
        """pedestrian 은 pedestrian_ai.generate() 의 반환값이어야 한다."""
        assert result["pedestrian"] == FAKE_PEDESTRIAN
        print(f"\n[PASS] pedestrian = {result['pedestrian']}")

    def test_traffic_comes_from_traffic_generator(self, result):
        """traffic 은 traffic_generator.generate() 의 반환값이어야 한다."""
        assert result["traffic"] == FAKE_TRAFFIC
        print(f"\n[PASS] traffic = {result['traffic']}")

    def test_corner_case_comes_from_corner_case_generator(self, result):
        """corner_case 는 corner_case_generator.generate() 의 반환값이어야 한다."""
        assert result["corner_case"] == FAKE_CORNER_CASE
        print(f"\n[PASS] corner_case = {result['corner_case']}")

    def test_scenario_type_is_string(self, result):
        """scenario_type 은 문자열이어야 한다."""
        assert isinstance(result["scenario_type"], str)

    def test_weather_is_dict(self, result):
        """weather 는 dict 여야 한다."""
        assert isinstance(result["weather"], dict)

    def test_pedestrian_is_dict(self, result):
        """pedestrian 은 dict 여야 한다."""
        assert isinstance(result["pedestrian"], dict)

    def test_traffic_is_dict(self, result):
        """traffic 은 dict 여야 한다."""
        assert isinstance(result["traffic"], dict)

    def test_corner_case_is_dict(self, result):
        """corner_case 는 dict 여야 한다."""
        assert isinstance(result["corner_case"], dict)


# =====================================================
# 반복 호출 안정성
# =====================================================
class TestRepeatability:

    def test_generate_called_multiple_times(self, gen):
        """generate() 를 10회 연속 호출해도 예외 없이 완료되어야 한다."""
        for i in range(10):
            result = gen.generate()
            assert isinstance(result, dict)
            assert result["scenario_type"] == "right_turn_pedestrian"
        print(f"\n[PASS] 10회 반복 호출 모두 유효")

    def test_sub_generators_called_n_times(self, gen):
        """generate() 를 5회 호출하면 각 하위 generator 도 5번씩 호출되어야 한다."""
        for _ in range(5):
            gen.generate()

        assert gen.weather_generator.generate.call_count     == 5
        assert gen.pedestrian_ai.generate.call_count         == 5
        assert gen.traffic_generator.generate.call_count     == 5
        assert gen.corner_case_generator.generate.call_count == 5
        print(f"\n[PASS] 5회 호출 → 각 하위 generator 5회 호출 확인")

    def test_each_call_returns_independent_result(self, gen):
        """generate() 를 여러 번 호출해도 각 결과가 독립적으로 반환되어야 한다."""
        gen.weather_generator.generate.side_effect = [
            {"condition": "clear"}, {"condition": "rain"}, {"condition": "fog"}
        ]
        gen.pedestrian_ai.generate.side_effect = [
            {"behavior": "normal_crossing"}, {"behavior": "jaywalking"}, {"behavior": "sudden_run"}
        ]
        gen.traffic_generator.generate.side_effect = [
            {"pattern": "light"}, {"pattern": "heavy"}, {"pattern": "moderate"}
        ]
        gen.corner_case_generator.generate.side_effect = [
            {"type": "sensor_failure"}, {"type": "pedestrian_occlusion"}, {"type": "sensor_failure"}
        ]

        results = [gen.generate() for _ in range(3)]

        assert results[0]["weather"]["condition"]   == "clear"
        assert results[1]["weather"]["condition"]   == "rain"
        assert results[2]["weather"]["condition"]   == "fog"
        assert results[0]["pedestrian"]["behavior"] == "normal_crossing"
        assert results[1]["traffic"]["pattern"]     == "heavy"
        print(f"\n[PASS] 3회 호출 결과 독립성 확인")
        for i, r in enumerate(results):
            print(f"       {i+1}번째: weather={r['weather']['condition']}, "
                  f"pedestrian={r['pedestrian']['behavior']}, "
                  f"traffic={r['traffic']['pattern']}")