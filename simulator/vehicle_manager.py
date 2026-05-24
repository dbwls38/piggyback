import airsim
import time
import random


class VehicleManager:

    def __init__(
        self,
        client
    ):

        self.client = client

    # =====================================
    # ENABLE API CONTROL
    # =====================================

    def enable_api_control(self):

        self.client.enableApiControl(
            True
        )

        print()

        print(
            "[API CONTROL ENABLED]"
        )

    # =====================================
    # DRIVE FORWARD
    # =====================================

    def drive_forward(self):

        controls = (
            airsim.CarControls()
        )

        controls.throttle = 0.7

        self.client.setCarControls(
            controls
        )

        print()

        print(
            "[VEHICLE MOVING FORWARD]"
        )

    # =====================================
    # TURN RIGHT
    # =====================================

    def right_turn(self):

        controls = (
            airsim.CarControls()
        )

        controls.throttle = 0.5

        controls.steering = 0.6

        self.client.setCarControls(
            controls
        )

        print()

        print(
            "[RIGHT TURN]"
        )

    # =====================================
    # AGGRESSIVE CUT-IN
    # =====================================

    def aggressive_cutin(self):

        controls = (
            airsim.CarControls()
        )

        controls.throttle = 0.9

        controls.steering = random.uniform(
            -0.8,
            0.8
        )

        self.client.setCarControls(
            controls
        )

        print()

        print(
            "[AGGRESSIVE CUT-IN]"
        )

    # =====================================
    # EMERGENCY BRAKE
    # =====================================

    def emergency_brake(self):

        controls = (
            airsim.CarControls()
        )

        controls.throttle = 0.0

        controls.brake = 1.0

        self.client.setCarControls(
            controls
        )

        print()

        print(
            "[EMERGENCY BRAKE]"
        )

    # =====================================
    # SET SPEED
    # =====================================

    def set_speed(
        self,
        speed_kmh
    ):

        controls = (
            airsim.CarControls()
        )

        throttle = min(
            speed_kmh / 40,
            1.0
        )

        controls.throttle = (
            throttle
        )

        self.client.setCarControls(
            controls
        )

        print()

        print(
            f"[VEHICLE SPEED] "
            f"{speed_kmh} km/h"
        )

    # =====================================
    # DEMO SCENARIO
    # =====================================

    def run_demo(self):

        print()

        print(
            "===== DEMO START ====="
        )

        # 직진
        self.drive_forward()

        time.sleep(3)

        # 우회전
        self.right_turn()

        time.sleep(3)

        # 위험 cut-in
        self.aggressive_cutin()

        time.sleep(3)

        # 긴급 제동
        self.emergency_brake()

        print()

        print(
            "===== DEMO END ====="
        )

    # =====================================
    # STOP VEHICLE
    # =====================================

    def stop_vehicle(self):

        controls = (
            airsim.CarControls()
        )

        controls.throttle = 0.0

        controls.brake = 1.0

        self.client.setCarControls(
            controls
        )

        print()

        print(
            "[VEHICLE STOPPED]"
        )

    # =====================================
    # DISABLE API CONTROL
    # =====================================

    def disable_api_control(self):

        self.client.enableApiControl(
            False
        )

        print()

        print(
            "[API CONTROL DISABLED]"
        )