#함수 호출 테스트 완료 #

import pytest
from unittest.mock import MagicMock, patch, call
# =====================================================
# HELPER: 매 테스트마다 airsim 모듈 자체를 통째로 교체
# =====================================================

def make_mock_airsim():
    """재사용 가능한 airsim 모킹 세트를 반환합니다."""
    mock_airsim = MagicMock()

    # WeatherParameter 상수
    mock_airsim.WeatherParameter.Rain        = "Rain"
    mock_airsim.WeatherParameter.Fog         = "Fog"
    mock_airsim.WeatherParameter.Roadwetness = "Roadwetness"

    # CarControls: 매번 새 MagicMock 반환
    fake_controls        = MagicMock()
    fake_controls.throttle = 0.0
    fake_controls.brake    = 0.0
    mock_airsim.CarControls.return_value = fake_controls

    # CarClient
    mock_client = MagicMock()
    mock_airsim.CarClient.return_value = mock_client

    return mock_airsim, mock_client, fake_controls


# =====================================================
# FIXTURES
# =====================================================

@pytest.fixture
def ctx():
    """
    airsim 모듈을 패치한 뒤 AirSimRunner 를 생성합니다.
    실제 AirSim 이 설치된 환경에서도 네트워크 연결 없이 동작합니다.

    yield 하는 값: (runner, mock_airsim, mock_client, fake_controls)
    """
    mock_airsim, mock_client, fake_controls = make_mock_airsim()

    # sys.modules["airsim"] 과 airsim_runner 내부의 airsim 참조를 동시에 교체
    with patch.dict("sys.modules", {"airsim": mock_airsim}):
        with patch("airsim_runner.airsim", mock_airsim):
            from airsim_runner import AirSimRunner
            runner = AirSimRunner()
            yield runner, mock_airsim, mock_client, fake_controls


# =====================================================
# __init__
# =====================================================

class TestInit:

    def test_confirm_connection_called(self, ctx):
        """초기화 시 confirmConnection() 이 호출되어야 한다."""
        runner, _, mock_client, _ = ctx
        mock_client.confirmConnection.assert_called_once()
        print("\n[PASS] confirmConnection 호출 확인")
        print(f"       호출 횟수: {mock_client.confirmConnection.call_count}")

    def test_api_control_enabled(self, ctx):
        """초기화 시 enableApiControl(True) 가 호출되어야 한다."""
        runner, _, mock_client, _ = ctx
        mock_client.enableApiControl.assert_called_with(True)
        print("\n[PASS] enableApiControl(True) 호출 확인")
        print(f"       전달된 인자: {mock_client.enableApiControl.call_args}")


# =====================================================
# apply_weather
# =====================================================
class TestApplyWeather:

    def test_always_enables_weather_sim(self, ctx):
        """어떤 날씨든 simEnableWeather(True) 가 항상 호출되어야 한다."""
        runner, _, mock_client, _ = ctx
        for condition in ["clear", "rain", "fog", "night"]:
            mock_client.reset_mock()
            runner.apply_weather({"condition": condition})
            mock_client.simEnableWeather.assert_called_with(True)
            print(f"\n[PASS] {condition:5s} → simEnableWeather(True) 확인")

    def test_clear_resets_rain_and_fog(self, ctx):
        """clear 날씨는 Rain=0.0, Fog=0.0 으로 리셋해야 한다."""
        runner, mock_airsim, mock_client, _ = ctx
        wp = mock_airsim.WeatherParameter
        runner.apply_weather({"condition": "clear"})
        calls = mock_client.simSetWeatherParameter.call_args_list
        assert call(wp.Rain, 0.0) in calls
        assert call(wp.Fog,  0.0) in calls
        print(f"\n[PASS] clear → 파라미터 설정 목록: {calls}")

    def test_rain_sets_rain_and_roadwetness(self, ctx):
        """rain 날씨는 Rain=0.8, Roadwetness=0.7 을 설정해야 한다."""
        runner, mock_airsim, mock_client, _ = ctx
        wp = mock_airsim.WeatherParameter
        runner.apply_weather({"condition": "rain"})
        calls = mock_client.simSetWeatherParameter.call_args_list
        assert call(wp.Rain,        0.8) in calls
        assert call(wp.Roadwetness, 0.7) in calls
        print(f"\n[PASS] rain → 파라미터 설정 목록: {calls}")

    def test_fog_sets_fog_value(self, ctx):
        """fog 날씨는 Fog=0.7 을 설정해야 한다."""
        runner, mock_airsim, mock_client, _ = ctx
        wp = mock_airsim.WeatherParameter
        runner.apply_weather({"condition": "fog"})
        mock_client.simSetWeatherParameter.assert_called_with(wp.Fog, 0.7)
        print(f"\n[PASS] fog → {mock_client.simSetWeatherParameter.call_args}")

    def test_night_sets_time_of_day(self, ctx):
        """night 날씨는 시간대를 22:00:00 으로 설정해야 한다."""
        runner, _, mock_client, _ = ctx
        runner.apply_weather({"condition": "night"})
        mock_client.simSetTimeOfDay.assert_called_with(True, "2025-01-01 22:00:00")
        print(f"\n[PASS] night → {mock_client.simSetTimeOfDay.call_args}")

    def test_unknown_condition_does_not_raise(self, ctx):
        """정의되지 않은 날씨 타입은 예외 없이 통과해야 한다."""
        runner, _, _, _ = ctx
        runner.apply_weather({"condition": "blizzard"})
        print("\n[PASS] 미정의 날씨 'blizzard' → 예외 없음")


# =====================================================
# apply_vehicle_speed
# =====================================================
class TestApplyVehicleSpeed:

    def test_50kmh_throttle_is_0_5(self, ctx):
        """50 km/h → throttle 0.5"""
        runner, mock_airsim, _, _ = ctx
        runner.apply_vehicle_speed(50)
        result = mock_airsim.CarControls.return_value.throttle
        assert result == pytest.approx(0.5)
        print(f"\n[PASS] 50 km/h → throttle = {result}")

    def test_throttle_capped_at_1(self, ctx):
        """200 km/h 초과 입력이어도 throttle 은 1.0 을 넘지 않아야 한다."""
        runner, mock_airsim, _, _ = ctx
        runner.apply_vehicle_speed(200)
        result = mock_airsim.CarControls.return_value.throttle
        assert result == pytest.approx(1.0)
        print(f"\n[PASS] 200 km/h → throttle = {result} (상한 1.0 적용)")

    def test_zero_speed_throttle_is_zero(self, ctx):
        """0 km/h → throttle 0.0"""
        runner, mock_airsim, _, _ = ctx
        runner.apply_vehicle_speed(0)
        result = mock_airsim.CarControls.return_value.throttle
        assert result == pytest.approx(0.0)
        print(f"\n[PASS] 0 km/h → throttle = {result}")

    def test_exactly_100kmh_throttle_is_1(self, ctx):
        """100 km/h → throttle 정확히 1.0"""
        runner, mock_airsim, _, _ = ctx
        runner.apply_vehicle_speed(100)
        result = mock_airsim.CarControls.return_value.throttle
        assert result == pytest.approx(1.0)
        print(f"\n[PASS] 100 km/h → throttle = {result}")

    def test_set_car_controls_is_called(self, ctx):
        """apply_vehicle_speed 호출 시 setCarControls 가 실행되어야 한다."""
        runner, _, mock_client, _ = ctx
        runner.apply_vehicle_speed(60)
        mock_client.setCarControls.assert_called_once()
        print(f"\n[PASS] setCarControls 호출 확인: {mock_client.setCarControls.call_args}")


# =====================================================
# apply_scenario
# =====================================================
class TestApplyScenario:

    @pytest.fixture
    def scenario(self):
        return {
            "weather":     {"condition": "rain"},
            "traffic":     {"average_speed": 60},
            "pedestrian":  {"count": 3, "behavior": "crossing"},
            "corner_case": {"type": "sudden_braking"},
        }

    def test_apply_weather_is_called(self, ctx, scenario):
        """apply_scenario 는 apply_weather 를 위임 호출해야 한다."""
        runner, _, _, _ = ctx
        with patch.object(runner, "apply_weather") as mw, \
             patch.object(runner, "apply_vehicle_speed"):
            runner.apply_scenario(scenario)
            mw.assert_called_once_with(scenario["weather"])
            print(f"\n[PASS] apply_weather 호출 인자: {mw.call_args}")

    def test_apply_vehicle_speed_is_called(self, ctx, scenario):
        """apply_scenario 는 average_speed 값으로 apply_vehicle_speed 를 호출해야 한다."""
        runner, _, _, _ = ctx
        with patch.object(runner, "apply_weather"), \
             patch.object(runner, "apply_vehicle_speed") as ms:
            runner.apply_scenario(scenario)
            ms.assert_called_once_with(60)
            print(f"\n[PASS] apply_vehicle_speed 호출 인자: {ms.call_args}")

    def test_full_scenario_no_exception(self, ctx, scenario):
        """apply_scenario 전체 흐름이 예외 없이 완료되어야 한다."""
        runner, _, _, _ = ctx
        runner.apply_scenario(scenario)
        print("\n[PASS] 전체 시나리오 예외 없이 완료")


# =====================================================
# shutdown
# =====================================================
class TestShutdown:

    def test_throttle_set_to_zero(self, ctx):
        """shutdown 시 throttle 은 0.0 이어야 한다."""
        runner, mock_airsim, _, _ = ctx
        runner.shutdown()
        result = mock_airsim.CarControls.return_value.throttle
        assert result == 0.0
        print(f"\n[PASS] shutdown → throttle = {result}")

    def test_brake_set_to_one(self, ctx):
        """shutdown 시 brake 는 1.0 이어야 한다."""
        runner, mock_airsim, _, _ = ctx
        runner.shutdown()
        result = mock_airsim.CarControls.return_value.brake
        assert result == 1.0
        print(f"\n[PASS] shutdown → brake = {result}")

    def test_set_car_controls_called(self, ctx):
        """shutdown 시 setCarControls 가 호출되어야 한다."""
        runner, _, mock_client, _ = ctx
        runner.shutdown()
        mock_client.setCarControls.assert_called_once()
        print(f"\n[PASS] setCarControls 호출 확인: {mock_client.setCarControls.call_args}")

    def test_api_control_disabled(self, ctx):
        """shutdown 시 enableApiControl(False) 가 호출되어야 한다."""
        runner, _, mock_client, _ = ctx
        runner.shutdown()
        mock_client.enableApiControl.assert_called_with(False)
        print(f"\n[PASS] enableApiControl(False) 확인: {mock_client.enableApiControl.call_args}")