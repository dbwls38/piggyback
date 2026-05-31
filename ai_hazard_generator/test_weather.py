#날씨 테스트#
import pytest
from unittest.mock import patch
from weather_generator import WeatherGenerator

VALID_CONDITIONS = ["clear", "rain", "heavy_rain", "fog", "night", "night_rain"]
VISIBILITY_MIN, VISIBILITY_MAX = 10, 100
FRICTION_MIN,   FRICTION_MAX   = 0.3, 1.0

# =====================================================
# FIXTURES
# =====================================================
@pytest.fixture
def gen():
    return WeatherGenerator()


# =====================================================
# 반환값 구조
# =====================================================
class TestReturnStructure:

    def test_returns_dict(self, gen):
        """generate() 는 dict 를 반환해야 한다."""
        result = gen.generate()
        assert isinstance(result, dict)
        print(f"\n[PASS] 반환 타입: {type(result).__name__}")

    def test_has_condition_key(self, gen):
        """반환값에 'condition' 키가 있어야 한다."""
        result = gen.generate()
        assert "condition" in result
        print(f"\n[PASS] 'condition' 키 존재 → 값: {result['condition']}")

    def test_has_visibility_distance_key(self, gen):
        """반환값에 'visibility_distance' 키가 있어야 한다."""
        result = gen.generate()
        assert "visibility_distance" in result
        print(f"\n[PASS] 'visibility_distance' 키 존재 → 값: {result['visibility_distance']}")

    def test_has_road_friction_key(self, gen):
        """반환값에 'road_friction' 키가 있어야 한다."""
        result = gen.generate()
        assert "road_friction" in result
        print(f"\n[PASS] 'road_friction' 키 존재 → 값: {result['road_friction']}")

    def test_no_extra_keys(self, gen):
        """'condition', 'visibility_distance', 'road_friction' 외 키가 없어야 한다."""
        result = gen.generate()
        assert set(result.keys()) == {"condition", "visibility_distance", "road_friction"}
        print(f"\n[PASS] 키 목록: {set(result.keys())}")


# =====================================================
# 반환값 유효성
# =====================================================
class TestReturnValues:

    def test_condition_is_valid(self, gen):
        """condition 은 정의된 목록 안에 있어야 한다."""
        result = gen.generate()
        assert result["condition"] in VALID_CONDITIONS
        print(f"\n[PASS] condition = '{result['condition']}' → 유효한 값")

    def test_condition_is_string(self, gen):
        """condition 은 문자열이어야 한다."""
        result = gen.generate()
        assert isinstance(result["condition"], str)

    def test_visibility_distance_is_int(self, gen):
        """visibility_distance 는 정수여야 한다."""
        result = gen.generate()
        assert isinstance(result["visibility_distance"], int)
        print(f"\n[PASS] visibility_distance 타입: {type(result['visibility_distance']).__name__}")

    def test_visibility_distance_within_range(self, gen):
        """visibility_distance 는 10 ~ 100 범위 안이어야 한다."""
        result = gen.generate()
        assert VISIBILITY_MIN <= result["visibility_distance"] <= VISIBILITY_MAX
        print(f"\n[PASS] visibility_distance = {result['visibility_distance']} (범위: {VISIBILITY_MIN}~{VISIBILITY_MAX})")

    def test_road_friction_is_float(self, gen):
        """road_friction 은 float 이어야 한다."""
        result = gen.generate()
        assert isinstance(result["road_friction"], float)
        print(f"\n[PASS] road_friction 타입: {type(result['road_friction']).__name__}")

    def test_road_friction_within_range(self, gen):
        """road_friction 은 0.3 ~ 1.0 범위 안이어야 한다."""
        result = gen.generate()
        assert FRICTION_MIN <= result["road_friction"] <= FRICTION_MAX
        print(f"\n[PASS] road_friction = {result['road_friction']} (범위: {FRICTION_MIN}~{FRICTION_MAX})")

    def test_road_friction_rounded_to_2_decimal(self, gen):
        """road_friction 은 소수점 2자리로 반올림되어야 한다."""
        result = gen.generate()
        assert result["road_friction"] == round(result["road_friction"], 2)
        print(f"\n[PASS] road_friction 소수점 2자리 확인: {result['road_friction']}")


# =====================================================
# random 함수 호출 여부
# =====================================================
class TestRandomCalled:

    def test_random_choice_called_once(self, gen):
        """generate() 에서 random.choice 가 정확히 1번 호출되어야 한다."""
        with patch("weather_generator.random.choice") as mock_choice, \
             patch("weather_generator.random.randint", return_value=50), \
             patch("weather_generator.random.uniform", return_value=0.7):
            mock_choice.return_value = "clear"
            gen.generate()

            assert mock_choice.call_count == 1
            print(f"\n[PASS] random.choice 호출 횟수: {mock_choice.call_count}")
            print(f"       호출 인자: {mock_choice.call_args}")

    def test_random_choice_uses_condition_list(self, gen):
        """random.choice 는 weather_conditions 리스트를 인자로 받아야 한다."""
        with patch("weather_generator.random.choice") as mock_choice, \
             patch("weather_generator.random.randint", return_value=50), \
             patch("weather_generator.random.uniform", return_value=0.7):
            mock_choice.return_value = "fog"
            gen.generate()

            arg = mock_choice.call_args[0][0]
            assert set(arg) == set(VALID_CONDITIONS)
            print(f"\n[PASS] choice 인자 목록: {arg}")

    def test_random_randint_called_once(self, gen):
        """generate() 에서 random.randint 가 정확히 1번 호출되어야 한다."""
        with patch("weather_generator.random.choice", return_value="rain"), \
             patch("weather_generator.random.randint") as mock_randint, \
             patch("weather_generator.random.uniform", return_value=0.6):
            mock_randint.return_value = 40
            gen.generate()

            assert mock_randint.call_count == 1
            print(f"\n[PASS] random.randint 호출 횟수: {mock_randint.call_count}")

    def test_random_randint_called_with_correct_range(self, gen):
        """random.randint 는 반드시 (10, 100) 인자로 호출되어야 한다."""
        with patch("weather_generator.random.choice", return_value="rain"), \
             patch("weather_generator.random.randint") as mock_randint, \
             patch("weather_generator.random.uniform", return_value=0.6):
            mock_randint.return_value = 40
            gen.generate()

            mock_randint.assert_called_once_with(10, 100)
            print(f"\n[PASS] random.randint 호출 인자: {mock_randint.call_args}")

    def test_random_uniform_called_once(self, gen):
        """generate() 에서 random.uniform 이 정확히 1번 호출되어야 한다."""
        with patch("weather_generator.random.choice", return_value="fog"), \
             patch("weather_generator.random.randint", return_value=30), \
             patch("weather_generator.random.uniform") as mock_uniform:
            mock_uniform.return_value = 0.55
            gen.generate()

            assert mock_uniform.call_count == 1
            print(f"\n[PASS] random.uniform 호출 횟수: {mock_uniform.call_count}")

    def test_random_uniform_called_with_correct_range(self, gen):
        """random.uniform 은 반드시 (0.3, 1.0) 인자로 호출되어야 한다."""
        with patch("weather_generator.random.choice", return_value="fog"), \
             patch("weather_generator.random.randint", return_value=30), \
             patch("weather_generator.random.uniform") as mock_uniform:
            mock_uniform.return_value = 0.55
            gen.generate()

            mock_uniform.assert_called_once_with(0.3, 1.0)
            print(f"\n[PASS] random.uniform 호출 인자: {mock_uniform.call_args}")


# =====================================================
# Mock 으로 결과 고정 테스트
# =====================================================
class TestGenerateWithMockedRandom:

    @pytest.mark.parametrize("condition,visibility,friction", [
        ("clear",      100, 1.0),
        ("rain",        60, 0.65),
        ("heavy_rain",  20, 0.35),
        ("fog",         15, 0.50),
        ("night",       80, 0.90),
        ("night_rain",  30, 0.40),
    ])
    def test_mocked_output_matches(self, gen, condition, visibility, friction):
        """random 을 고정하면 반환값이 정확히 일치해야 한다."""
        with patch("weather_generator.random.choice", return_value=condition), \
             patch("weather_generator.random.randint", return_value=visibility), \
             patch("weather_generator.random.uniform", return_value=friction):
            result = gen.generate()

            assert result == {
                "condition":           condition,
                "visibility_distance": visibility,
                "road_friction":       round(friction, 2),
            }
            print(f"\n[PASS] {result}")

    def test_road_friction_is_rounded_from_uniform(self, gen):
        """random.uniform 의 긴 소수값이 round(2) 처리되어야 한다."""
        with patch("weather_generator.random.choice", return_value="rain"), \
             patch("weather_generator.random.randint", return_value=50), \
             patch("weather_generator.random.uniform", return_value=0.56789):
            result = gen.generate()

            assert result["road_friction"] == 0.57
            print(f"\n[PASS] uniform(0.56789) → road_friction = {result['road_friction']}")

    def test_visibility_distance_boundary_min(self, gen):
        """visibility_distance 경계 최솟값 10 이 그대로 반환되어야 한다."""
        with patch("weather_generator.random.choice", return_value="heavy_rain"), \
             patch("weather_generator.random.randint", return_value=10), \
             patch("weather_generator.random.uniform", return_value=0.3):
            result = gen.generate()

            assert result["visibility_distance"] == 10
            print(f"\n[PASS] visibility_distance 최솟값: {result['visibility_distance']}")

    def test_visibility_distance_boundary_max(self, gen):
        """visibility_distance 경계 최댓값 100 이 그대로 반환되어야 한다."""
        with patch("weather_generator.random.choice", return_value="clear"), \
             patch("weather_generator.random.randint", return_value=100), \
             patch("weather_generator.random.uniform", return_value=1.0):
            result = gen.generate()

            assert result["visibility_distance"] == 100
            print(f"\n[PASS] visibility_distance 최댓값: {result['visibility_distance']}")


# =====================================================
# 반복 호출 안정성
# =====================================================
class TestRepeatability:

    def test_always_returns_valid_result(self, gen):
        """100회 반복 호출해도 항상 유효한 결과를 반환해야 한다."""
        for _ in range(100):
            result = gen.generate()
            assert result["condition"]           in VALID_CONDITIONS
            assert VISIBILITY_MIN <= result["visibility_distance"] <= VISIBILITY_MAX
            assert FRICTION_MIN   <= result["road_friction"]       <= FRICTION_MAX
        print(f"\n[PASS] 100회 반복 호출 모두 유효")

    def test_covers_all_conditions(self, gen):
        """충분히 많이 호출하면 모든 condition 이 등장해야 한다."""
        seen = set()
        for _ in range(500):
            seen.add(gen.generate()["condition"])
        assert seen == set(VALID_CONDITIONS)
        print(f"\n[PASS] 500회 후 등장한 condition: {seen}")

    def test_visibility_distance_range_boundary(self, gen):
        """200회 호출 시 visibility_distance 가 항상 경계값 내에 있어야 한다."""
        values = [gen.generate()["visibility_distance"] for _ in range(200)]
        assert all(VISIBILITY_MIN <= v <= VISIBILITY_MAX for v in values)
        print(f"\n[PASS] visibility_distance 범위 확인 → min={min(values)}, max={max(values)}")

    def test_road_friction_range_boundary(self, gen):
        """200회 호출 시 road_friction 이 항상 경계값 내에 있어야 한다."""
        values = [gen.generate()["road_friction"] for _ in range(200)]
        assert all(FRICTION_MIN <= v <= FRICTION_MAX for v in values)
        print(f"\n[PASS] road_friction 범위 확인 → min={min(values)}, max={max(values)}")