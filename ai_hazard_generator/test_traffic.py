#traffic함수 호출 테스트 완료#
import pytest
from unittest.mock import patch
from traffic_pattern_generator import TrafficPatternGenerator

VALID_PATTERNS  = ["light", "moderate", "heavy", "aggressive_cutin", "signal_violation"]
DENSITY_MIN,  DENSITY_MAX  = 5,  50
SPEED_MIN,    SPEED_MAX    = 20, 80

# =====================================================
# FIXTURES
# =====================================================
@pytest.fixture
def gen():
    return TrafficPatternGenerator()


# =====================================================
# 반환값 구조
# =====================================================
class TestReturnStructure:

    def test_returns_dict(self, gen):
        """generate() 는 dict 를 반환해야 한다."""
        result = gen.generate()
        assert isinstance(result, dict)
        print(f"\n[PASS] 반환 타입: {type(result).__name__}")

    def test_has_pattern_key(self, gen):
        """반환값에 'pattern' 키가 있어야 한다."""
        result = gen.generate()
        assert "pattern" in result
        print(f"\n[PASS] 'pattern' 키 존재 → 값: {result['pattern']}")

    def test_has_vehicle_density_key(self, gen):
        """반환값에 'vehicle_density' 키가 있어야 한다."""
        result = gen.generate()
        assert "vehicle_density" in result
        print(f"\n[PASS] 'vehicle_density' 키 존재 → 값: {result['vehicle_density']}")

    def test_has_average_speed_key(self, gen):
        """반환값에 'average_speed' 키가 있어야 한다."""
        result = gen.generate()
        assert "average_speed" in result
        print(f"\n[PASS] 'average_speed' 키 존재 → 값: {result['average_speed']}")

    def test_no_extra_keys(self, gen):
        """'pattern', 'vehicle_density', 'average_speed' 외 키가 없어야 한다."""
        result = gen.generate()
        assert set(result.keys()) == {"pattern", "vehicle_density", "average_speed"}
        print(f"\n[PASS] 키 목록: {set(result.keys())}")


# =====================================================
# 반환값 유효성
# =====================================================
class TestReturnValues:

    def test_pattern_is_valid(self, gen):
        """pattern 은 정의된 목록 안에 있어야 한다."""
        result = gen.generate()
        assert result["pattern"] in VALID_PATTERNS
        print(f"\n[PASS] pattern = '{result['pattern']}' → 유효한 값")

    def test_pattern_is_string(self, gen):
        """pattern 은 문자열이어야 한다."""
        result = gen.generate()
        assert isinstance(result["pattern"], str)

    def test_vehicle_density_is_int(self, gen):
        """vehicle_density 는 정수여야 한다."""
        result = gen.generate()
        assert isinstance(result["vehicle_density"], int)
        print(f"\n[PASS] vehicle_density 타입: {type(result['vehicle_density']).__name__}")

    def test_vehicle_density_within_range(self, gen):
        """vehicle_density 는 5 ~ 50 범위 안이어야 한다."""
        result = gen.generate()
        assert DENSITY_MIN <= result["vehicle_density"] <= DENSITY_MAX
        print(f"\n[PASS] vehicle_density = {result['vehicle_density']} (범위: {DENSITY_MIN}~{DENSITY_MAX})")

    def test_average_speed_is_int(self, gen):
        """average_speed 는 정수여야 한다."""
        result = gen.generate()
        assert isinstance(result["average_speed"], int)
        print(f"\n[PASS] average_speed 타입: {type(result['average_speed']).__name__}")

    def test_average_speed_within_range(self, gen):
        """average_speed 는 20 ~ 80 범위 안이어야 한다."""
        result = gen.generate()
        assert SPEED_MIN <= result["average_speed"] <= SPEED_MAX
        print(f"\n[PASS] average_speed = {result['average_speed']} (범위: {SPEED_MIN}~{SPEED_MAX})")


# =====================================================
# random 함수 호출 여부
# =====================================================
class TestRandomCalled:

    def test_random_choice_called_once(self, gen):
        """generate() 에서 random.choice 가 정확히 1번 호출되어야 한다."""
        with patch("traffic_pattern_generator.random.choice") as mock_choice, \
             patch("traffic_pattern_generator.random.randint", return_value=30):
            mock_choice.return_value = "light"
            gen.generate()

            assert mock_choice.call_count == 1
            print(f"\n[PASS] random.choice 호출 횟수: {mock_choice.call_count}")
            print(f"       호출 인자: {mock_choice.call_args}")

    def test_random_choice_uses_pattern_list(self, gen):
        """random.choice 는 traffic_patterns 리스트를 인자로 받아야 한다."""
        with patch("traffic_pattern_generator.random.choice") as mock_choice, \
             patch("traffic_pattern_generator.random.randint", return_value=30):
            mock_choice.return_value = "heavy"
            gen.generate()

            arg = mock_choice.call_args[0][0]
            assert set(arg) == set(VALID_PATTERNS)
            print(f"\n[PASS] choice 인자 목록: {arg}")

    def test_random_randint_called_twice(self, gen):
        """generate() 에서 random.randint 가 정확히 2번 호출되어야 한다."""
        with patch("traffic_pattern_generator.random.choice", return_value="moderate"), \
             patch("traffic_pattern_generator.random.randint") as mock_randint:
            mock_randint.side_effect = [25, 60]
            gen.generate()

            assert mock_randint.call_count == 2
            print(f"\n[PASS] random.randint 호출 횟수: {mock_randint.call_count}")
            for i, c in enumerate(mock_randint.call_args_list, 1):
                print(f"       {i}번째 호출 인자: {c}")

    def test_first_randint_uses_density_range(self, gen):
        """첫 번째 random.randint 는 (5, 50) 인자로 호출되어야 한다."""
        with patch("traffic_pattern_generator.random.choice", return_value="light"), \
             patch("traffic_pattern_generator.random.randint") as mock_randint:
            mock_randint.side_effect = [10, 40]
            gen.generate()

            first_call_args = mock_randint.call_args_list[0][0]
            assert first_call_args == (5, 50)
            print(f"\n[PASS] 1번째 randint 인자: {first_call_args}")

    def test_second_randint_uses_speed_range(self, gen):
        """두 번째 random.randint 는 (20, 80) 인자로 호출되어야 한다."""
        with patch("traffic_pattern_generator.random.choice", return_value="light"), \
             patch("traffic_pattern_generator.random.randint") as mock_randint:
            mock_randint.side_effect = [10, 40]
            gen.generate()

            second_call_args = mock_randint.call_args_list[1][0]
            assert second_call_args == (20, 80)
            print(f"\n[PASS] 2번째 randint 인자: {second_call_args}")


# =====================================================
# Mock 으로 결과 고정 테스트
# =====================================================
class TestGenerateWithMockedRandom:

    @pytest.mark.parametrize("pattern,density,speed", [
        ("light",             5,  20),
        ("moderate",         25,  50),
        ("heavy",            50,  80),
        ("aggressive_cutin", 40,  70),
        ("signal_violation", 15,  35),
    ])
    def test_mocked_output_matches(self, gen, pattern, density, speed):
        """random 을 고정하면 반환값이 정확히 일치해야 한다."""
        with patch("traffic_pattern_generator.random.choice", return_value=pattern), \
             patch("traffic_pattern_generator.random.randint", side_effect=[density, speed]):
            result = gen.generate()

            assert result == {
                "pattern":        pattern,
                "vehicle_density": density,
                "average_speed":  speed,
            }
            print(f"\n[PASS] {result}")

    def test_density_boundary_min(self, gen):
        """vehicle_density 경계 최솟값 5 가 그대로 반환되어야 한다."""
        with patch("traffic_pattern_generator.random.choice", return_value="heavy"), \
             patch("traffic_pattern_generator.random.randint", side_effect=[5, 20]):
            result = gen.generate()
            assert result["vehicle_density"] == 5
            print(f"\n[PASS] vehicle_density 최솟값: {result['vehicle_density']}")

    def test_density_boundary_max(self, gen):
        """vehicle_density 경계 최댓값 50 이 그대로 반환되어야 한다."""
        with patch("traffic_pattern_generator.random.choice", return_value="heavy"), \
             patch("traffic_pattern_generator.random.randint", side_effect=[50, 80]):
            result = gen.generate()
            assert result["vehicle_density"] == 50
            print(f"\n[PASS] vehicle_density 최댓값: {result['vehicle_density']}")

    def test_speed_boundary_min(self, gen):
        """average_speed 경계 최솟값 20 이 그대로 반환되어야 한다."""
        with patch("traffic_pattern_generator.random.choice", return_value="light"), \
             patch("traffic_pattern_generator.random.randint", side_effect=[5, 20]):
            result = gen.generate()
            assert result["average_speed"] == 20
            print(f"\n[PASS] average_speed 최솟값: {result['average_speed']}")

    def test_speed_boundary_max(self, gen):
        """average_speed 경계 최댓값 80 이 그대로 반환되어야 한다."""
        with patch("traffic_pattern_generator.random.choice", return_value="light"), \
             patch("traffic_pattern_generator.random.randint", side_effect=[50, 80]):
            result = gen.generate()
            assert result["average_speed"] == 80
            print(f"\n[PASS] average_speed 최댓값: {result['average_speed']}")


# =====================================================
# 반복 호출 안정성
# =====================================================
class TestRepeatability:

    def test_always_returns_valid_result(self, gen):
        """100회 반복 호출해도 항상 유효한 결과를 반환해야 한다."""
        for _ in range(100):
            result = gen.generate()
            assert result["pattern"]         in VALID_PATTERNS
            assert DENSITY_MIN <= result["vehicle_density"] <= DENSITY_MAX
            assert SPEED_MIN   <= result["average_speed"]   <= SPEED_MAX
        print(f"\n[PASS] 100회 반복 호출 모두 유효")

    def test_covers_all_patterns(self, gen):
        """충분히 많이 호출하면 모든 pattern 이 등장해야 한다."""
        seen = set()
        for _ in range(500):
            seen.add(gen.generate()["pattern"])
        assert seen == set(VALID_PATTERNS)
        print(f"\n[PASS] 500회 후 등장한 pattern: {seen}")

    def test_vehicle_density_range_boundary(self, gen):
        """200회 호출 시 vehicle_density 가 항상 경계값 내에 있어야 한다."""
        values = [gen.generate()["vehicle_density"] for _ in range(200)]
        assert all(DENSITY_MIN <= v <= DENSITY_MAX for v in values)
        print(f"\n[PASS] vehicle_density 범위 → min={min(values)}, max={max(values)}")

    def test_average_speed_range_boundary(self, gen):
        """200회 호출 시 average_speed 가 항상 경계값 내에 있어야 한다."""
        values = [gen.generate()["average_speed"] for _ in range(200)]
        assert all(SPEED_MIN <= v <= SPEED_MAX for v in values)
        print(f"\n[PASS] average_speed 범위 → min={min(values)}, max={max(values)}")