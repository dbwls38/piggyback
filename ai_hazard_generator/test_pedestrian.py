#보행자 테스트 완료#
import pytest
from unittest.mock import patch, call
from pedestrian_behavior_ai import PedestrianBehaviorAI

VALID_BEHAVIORS   = ["normal_crossing", "jaywalking", "sudden_run", "phone_distracted", "slow_crossing"]
VALID_VISIBILITIES = ["high", "medium", "low"]
SPEED_MIN, SPEED_MAX = 0.5, 2.5

# =====================================================
# FIXTURES
# =====================================================

@pytest.fixture
def ai():
    return PedestrianBehaviorAI()


# =====================================================
# 반환값 구조
# =====================================================
class TestReturnStructure:

    def test_returns_dict(self, ai):
        """generate() 는 dict 를 반환해야 한다."""
        result = ai.generate()
        assert isinstance(result, dict)
        print(f"\n[PASS] 반환 타입: {type(result).__name__}")

    def test_has_behavior_key(self, ai):
        """반환값에 'behavior' 키가 있어야 한다."""
        result = ai.generate()
        assert "behavior" in result
        print(f"\n[PASS] 'behavior' 키 존재 → 값: {result['behavior']}")

    def test_has_speed_key(self, ai):
        """반환값에 'speed' 키가 있어야 한다."""
        result = ai.generate()
        assert "speed" in result
        print(f"\n[PASS] 'speed' 키 존재 → 값: {result['speed']}")

    def test_has_visibility_key(self, ai):
        """반환값에 'visibility' 키가 있어야 한다."""
        result = ai.generate()
        assert "visibility" in result
        print(f"\n[PASS] 'visibility' 키 존재 → 값: {result['visibility']}")

    def test_no_extra_keys(self, ai):
        """'behavior', 'speed', 'visibility' 외 불필요한 키가 없어야 한다."""
        result = ai.generate()
        assert set(result.keys()) == {"behavior", "speed", "visibility"}
        print(f"\n[PASS] 키 목록: {set(result.keys())}")


# =====================================================
# 반환값 유효성
# =====================================================
class TestReturnValues:

    def test_behavior_is_valid(self, ai):
        """behavior 는 정의된 목록 안에 있어야 한다."""
        result = ai.generate()
        assert result["behavior"] in VALID_BEHAVIORS
        print(f"\n[PASS] behavior = '{result['behavior']}' → 유효한 값")

    def test_behavior_is_string(self, ai):
        """behavior 는 문자열이어야 한다."""
        result = ai.generate()
        assert isinstance(result["behavior"], str)

    def test_speed_is_float(self, ai):
        """speed 는 float 이어야 한다."""
        result = ai.generate()
        assert isinstance(result["speed"], float)
        print(f"\n[PASS] speed 타입: {type(result['speed']).__name__}")

    def test_speed_within_range(self, ai):
        """speed 는 0.5 ~ 2.5 범위 안이어야 한다."""
        result = ai.generate()
        assert SPEED_MIN <= result["speed"] <= SPEED_MAX
        print(f"\n[PASS] speed = {result['speed']} (범위: {SPEED_MIN}~{SPEED_MAX})")

    def test_speed_rounded_to_2_decimal(self, ai):
        """speed 는 소수점 2자리로 반올림되어야 한다."""
        result = ai.generate()
        assert result["speed"] == round(result["speed"], 2)
        print(f"\n[PASS] speed 소수점 2자리 확인: {result['speed']}")

    def test_visibility_is_valid(self, ai):
        """visibility 는 high / medium / low 중 하나여야 한다."""
        result = ai.generate()
        assert result["visibility"] in VALID_VISIBILITIES
        print(f"\n[PASS] visibility = '{result['visibility']}' → 유효한 값")

    def test_visibility_is_string(self, ai):
        """visibility 는 문자열이어야 한다."""
        result = ai.generate()
        assert isinstance(result["visibility"], str)


# =====================================================
# random 함수 호출 여부
# =====================================================
class TestRandomCalled:

    def test_random_choice_called_twice(self, ai):
        """generate() 에서 random.choice 가 정확히 2번 호출되어야 한다."""
        with patch("pedestrian_behavior_ai.random.choice") as mock_choice, \
             patch("pedestrian_behavior_ai.random.uniform", return_value=1.5):
            mock_choice.side_effect = ["jaywalking", "medium"]
            ai.generate()

            assert mock_choice.call_count == 2
            print(f"\n[PASS] random.choice 호출 횟수: {mock_choice.call_count}")
            for i, c in enumerate(mock_choice.call_args_list, 1):
                print(f"       {i}번째 호출 인자: {c}")

    def test_random_uniform_called_once(self, ai):
        """generate() 에서 random.uniform 이 정확히 1번 호출되어야 한다."""
        with patch("pedestrian_behavior_ai.random.choice") as mock_choice, \
             patch("pedestrian_behavior_ai.random.uniform") as mock_uniform:
            mock_choice.side_effect = ["sudden_run", "high"]
            mock_uniform.return_value = 1.23
            ai.generate()

            assert mock_uniform.call_count == 1
            print(f"\n[PASS] random.uniform 호출 횟수: {mock_uniform.call_count}")

    def test_random_uniform_called_with_correct_range(self, ai):
        """random.uniform 은 반드시 (0.5, 2.5) 인자로 호출되어야 한다."""
        with patch("pedestrian_behavior_ai.random.choice") as mock_choice, \
             patch("pedestrian_behavior_ai.random.uniform") as mock_uniform:
            mock_choice.side_effect = ["normal_crossing", "low"]
            mock_uniform.return_value = 1.0
            ai.generate()

            mock_uniform.assert_called_once_with(0.5, 2.5)
            print(f"\n[PASS] random.uniform 호출 인자: {mock_uniform.call_args}")

    def test_first_choice_uses_behavior_list(self, ai):
        """첫 번째 random.choice 는 behaviors 리스트를 인자로 받아야 한다."""
        with patch("pedestrian_behavior_ai.random.choice") as mock_choice, \
             patch("pedestrian_behavior_ai.random.uniform", return_value=1.0):
            mock_choice.side_effect = ["jaywalking", "high"]
            ai.generate()

            first_arg = mock_choice.call_args_list[0][0][0]
            assert set(first_arg) == set(VALID_BEHAVIORS)
            print(f"\n[PASS] 1번째 choice 인자: {first_arg}")

    def test_second_choice_uses_visibility_list(self, ai):
        """두 번째 random.choice 는 visibility 리스트를 인자로 받아야 한다."""
        with patch("pedestrian_behavior_ai.random.choice") as mock_choice, \
             patch("pedestrian_behavior_ai.random.uniform", return_value=1.0):
            mock_choice.side_effect = ["jaywalking", "high"]
            ai.generate()

            second_arg = mock_choice.call_args_list[1][0][0]
            assert set(second_arg) == set(VALID_VISIBILITIES)
            print(f"\n[PASS] 2번째 choice 인자: {second_arg}")


# =====================================================
# Mock 으로 결과 고정 테스트
# =====================================================
class TestGenerateWithMockedRandom:

    @pytest.mark.parametrize("behavior,speed,visibility", [
        ("normal_crossing",  1.20, "high"),
        ("jaywalking",       2.50, "low"),
        ("sudden_run",       0.50, "medium"),
        ("phone_distracted", 1.75, "high"),
        ("slow_crossing",    0.80, "low"),
    ])
    def test_mocked_output_matches(self, ai, behavior, speed, visibility):
        """random 을 고정하면 반환값이 정확히 일치해야 한다."""
        with patch("pedestrian_behavior_ai.random.choice") as mock_choice, \
             patch("pedestrian_behavior_ai.random.uniform", return_value=speed):
            mock_choice.side_effect = [behavior, visibility]
            result = ai.generate()

            assert result == {
                "behavior":   behavior,
                "speed":      round(speed, 2),
                "visibility": visibility,
            }
            print(f"\n[PASS] {result}")

    def test_speed_is_rounded_from_uniform(self, ai):
        """random.uniform 의 긴 소수값이 round(2) 처리되어야 한다."""
        with patch("pedestrian_behavior_ai.random.choice") as mock_choice, \
             patch("pedestrian_behavior_ai.random.uniform", return_value=1.23456789):
            mock_choice.side_effect = ["sudden_run", "medium"]
            result = ai.generate()

            assert result["speed"] == 1.23
            print(f"\n[PASS] uniform(1.23456789) → speed = {result['speed']}")


# =====================================================
# 반복 호출 안정성
# =====================================================
class TestRepeatability:

    def test_always_returns_valid_result(self, ai):
        """50회 반복 호출해도 항상 유효한 결과를 반환해야 한다."""
        for i in range(50):
            result = ai.generate()
            assert result["behavior"]   in VALID_BEHAVIORS
            assert result["visibility"] in VALID_VISIBILITIES
            assert SPEED_MIN <= result["speed"] <= SPEED_MAX
        print(f"\n[PASS] 50회 반복 호출 모두 유효")

    def test_covers_all_behaviors(self, ai):
        """충분히 많이 호출하면 모든 behavior 가 등장해야 한다."""
        seen = set()
        for _ in range(300):
            seen.add(ai.generate()["behavior"])
        assert seen == set(VALID_BEHAVIORS)
        print(f"\n[PASS] 300회 후 등장한 behavior: {seen}")

    def test_covers_all_visibilities(self, ai):
        """충분히 많이 호출하면 모든 visibility 가 등장해야 한다."""
        seen = set()
        for _ in range(100):
            seen.add(ai.generate()["visibility"])
        assert seen == set(VALID_VISIBILITIES)
        print(f"\n[PASS] 100회 후 등장한 visibility: {seen}")

    def test_speed_range_boundary(self, ai):
        """200회 호출 시 speed 가 항상 경계값 내에 있어야 한다."""
        speeds = [ai.generate()["speed"] for _ in range(200)]
        assert all(SPEED_MIN <= s <= SPEED_MAX for s in speeds)
        print(f"\n[PASS] speed 범위 확인 → min={min(speeds)}, max={max(speeds)}")