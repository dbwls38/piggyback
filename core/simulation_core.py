class SimulationCore:

    def __init__(self, airsim_service, scenario_engine, hara_engine):
        self.airsim = airsim_service
        self.scenario_engine = scenario_engine
        self.hara_engine = hara_engine

        self.current_scenario = None
        self.current_state = "IDLE"

    # -------------------------
    # 1. 시나리오 실행
    # -------------------------
    def run_scenario(self, scenario_type):

        print(f"[Core] Running scenario: {scenario_type}")

        # 1) 시나리오 생성
        scenario = self.scenario_engine.generate(scenario_type)
        self.current_scenario = scenario

        # 2) AirSim 적용
        self._apply_to_airsim(scenario)

        # 3) 상태 변경
        self.current_state = "RUNNING"

        # 4) HARA 실행
        risk = self.hara_engine.evaluate(scenario)

        return {
            "scenario": scenario,
            "risk": risk,
            "state": self.current_state
        }

    # -------------------------
    # 2. AirSim 적용
    # -------------------------
    def _apply_to_airsim(self, scenario):

        print("[Core] Applying scenario to AirSim")

        if scenario.get("pedestrian"):
            print("[Core] Pedestrian enabled")

        speed = scenario.get("vehicle_speed", 30)

        self.airsim.client.setCarControls(
            self.airsim.client.CarControls(
                throttle=speed / 100
            )
        )

    # -------------------------
    # 3. 시작
    # -------------------------
    def start(self):
        print("[Core] Simulation start")
        self.current_state = "RUNNING"
        self.airsim.start()

    # -------------------------
    # 4. 정지
    # -------------------------
    def stop(self):
        print("[Core] Simulation stop")
        self.current_state = "STOPPED"
        self.airsim.stop()

    # -------------------------
    # 5. 상태 조회
    # -------------------------
    def get_state(self):
        return {
            "state": self.current_state,
            "scenario": self.current_scenario,
            "risk": self.hara_engine.evaluate(self.current_scenario)
        }

    def get_state(self):
        scenario = self.current_scenario

        risk = self.hara_engine.evaluate(scenario)

        return {
            "state": self.current_state,
            "scenario": scenario,
            "ASIL": risk["ASIL"],
            "collision": risk["collision"],
            "speed": risk["speed"]
        }