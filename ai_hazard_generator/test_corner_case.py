#코너 테스트 완료#
import pytest
from unittest.mock import patch
from corner_case_generator import CornerCaseGenerator

VALID_TYPES = [
    "pedestrian_occlusion",
    "sudden_vehicle_cutin",
    "sensor_failure",
    "traffic_light_failure",
    "blind_spot_pedestrian",
    "unexpected_braking",
    "wrong_way_vehicle",
]

VALID_RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


# =====================================================
# FIXTURES
# =====================================================

@pytest.fixture
def generator():
    return CornerCaseGenerator()


# =====================================================
# generate() 반환값 구조
# =====================================================

class TestGenerateReturnStructure:

    def test_returns_dict(self, generator):
        """generate() 는 dict 를 반환해야 한다."""
        result = generator.generate()
        assert isinstance(result, dict)
        print(f"\n[PASS] 반환 타입: {type(result).__name__}")

    def test_has_type_key(self, generator):
        """반환값에 'type' 키가 있어야 한다."""
        result = generator.generate()
        assert "type" in result
        print(f"\n[PASS] 'type' 키 존재 → 값: {result['type']}")

    def test_has_risk_level_key(self, generator):
        """반환값에 'risk_level' 키가 있어야 한다."""
        result = generator.generate()
        assert "risk_level" in result
        print(f"\n[PASS] 'risk_level' 키 존재 → 값: {result['risk_level']}")

    def test_no_extra_keys(self, generator):
        """반환값에 'type', 'risk_level' 외 불필요한 키가 없어야 한다."""
        result = generator.generate()
        assert set(result.keys()) == {"type", "risk_level"}
        print(f"\n[PASS] 키 목록: {set(result.keys())}")


# =====================================================
# generate() 반환값 유효성
# =====================================================
class TestGenerateValues:

    def test_type_is_valid(self, generator):
        """반환된 type 은 정의된 목록 안에 있어야 한다."""
        result = generator.generate()
        assert result["type"] in VALID_TYPES
        print(f"\n[PASS] type = '{result['type']}' → 유효한 값")

    def test_risk_level_is_valid(self, generator):
        """반환된 risk_level 은 LOW/MEDIUM/HIGH/CRITICAL 중 하나여야 한다."""
        result = generator.generate()
        assert result["risk_level"] in VALID_RISK_LEVELS
        print(f"\n[PASS] risk_level = '{result['risk_level']}' → 유효한 값")

    def test_type_is_string(self, generator):
        """type 값은 문자열이어야 한다."""
        result = generator.generate()
        assert isinstance(result["type"], str)

    def test_risk_level_is_string(self, generator):
        """risk_level 값은 문자열이어야 한다."""
        result = generator.generate()
        assert isinstance(result["risk_level"], str)


# =====================================================
# random.choice 호출 여부 (Mock)
# =====================================================
class TestRandomChoiceCalled:

    def test_random_choice_called_twice(self, generator):
        """generate() 내부에서 random.choice 가 정확히 2번 호출되어야 한다."""
        with patch("corner_case_generator.random.choice") as mock_choice:
            mock_choice.side_effect = ["sensor_failure", "HIGH"]
            generator.generate()

            assert mock_choice.call_count == 2
            print(f"\n[PASS] random.choice 호출 횟수: {mock_choice.call_count}")
            print(f"       호출 인자 목록:")
            for i, c in enumerate(mock_choice.call_args_list, 1):
                print(f"         {i}번째: {c}")

    def test_first_call_uses_corner_case_list(self, generator):
        """첫 번째 random.choice 는 corner_cases 리스트를 인자로 받아야 한다."""
        with patch("corner_case_generator.random.choice") as mock_choice:
            mock_choice.side_effect = ["sensor_failure", "HIGH"]
            generator.generate()

            first_arg = mock_choice.call_args_list[0][0][0]
            assert set(first_arg) == set(VALID_TYPES)
            print(f"\n[PASS] 1번째 호출 인자: {first_arg}")

    def test_second_call_uses_risk_level_list(self, generator):
        """두 번째 random.choice 는 risk_level 리스트를 인자로 받아야 한다."""
        with patch("corner_case_generator.random.choice") as mock_choice:
            mock_choice.side_effect = ["sensor_failure", "HIGH"]
            generator.generate()

            second_arg = mock_choice.call_args_list[1][0][0]
            assert set(second_arg) == set(VALID_RISK_LEVELS)
            print(f"\n[PASS] 2번째 호출 인자: {second_arg}")


# =====================================================
# Mock 으로 결과 고정 테스트
# =====================================================
class TestGenerateWithMockedRandom:

    @pytest.mark.parametrize("case_type,risk", [
        ("sensor_failure",       "HIGH"),
        ("wrong_way_vehicle",    "CRITICAL"),
        ("pedestrian_occlusion", "LOW"),
        ("unexpected_braking",   "MEDIUM"),
    ])
    def test_mocked_output_matches(self, generator, case_type, risk):
        """random.choice 를 고정하면 반환값이 정확히 일치해야 한다."""
        with patch("corner_case_generator.random.choice") as mock_choice:
            mock_choice.side_effect = [case_type, risk]
            result = generator.generate()

            assert result == {"type": case_type, "risk_level": risk}
            print(f"\n[PASS] type={case_type}, risk_level={risk} → {result}")

    def test_generate_returns_mocked_type(self, generator):
        """Mock 으로 type 을 고정했을 때 반환값의 type 이 일치해야 한다."""
        with patch("corner_case_generator.random.choice") as mock_choice:
            mock_choice.side_effect = ["sudden_vehicle_cutin", "CRITICAL"]
            result = generator.generate()

            assert result["type"] == "sudden_vehicle_cutin"
            assert result["risk_level"] == "CRITICAL"
            print(f"\n[PASS] 고정 결과: {result}")


# =====================================================
# 반복 호출 안정성
# =====================================================
class TestGenerateRepeatability:

    def test_generate_called_multiple_times(self, generator):
        """generate() 를 여러 번 호출해도 항상 유효한 결과를 반환해야 한다."""
        for i in range(20):
            result = generator.generate()
            assert result["type"] in VALID_TYPES
            assert result["risk_level"] in VALID_RISK_LEVELS
        print(f"\n[PASS] 20회 반복 호출 모두 유효한 값 반환")

    def test_generate_covers_all_types_eventually(self, generator):
        """충분히 많이 호출하면 모든 type 이 최소 1번은 등장해야 한다."""
        seen_types = set()
        for _ in range(200):
            result = generator.generate()
            seen_types.add(result["type"])

        assert seen_types == set(VALID_TYPES)
        print(f"\n[PASS] 200회 호출 후 등장한 type 목록: {seen_types}")

    def test_generate_covers_all_risk_levels_eventually(self, generator):
        """충분히 많이 호출하면 모든 risk_level 이 최소 1번은 등장해야 한다."""
        seen_risks = set()
        for _ in range(100):
            result = generator.generate()
            seen_risks.add(result["risk_level"])

        assert seen_risks == set(VALID_RISK_LEVELS)
        print(f"\n[PASS] 100회 호출 후 등장한 risk_level: {seen_risks}")