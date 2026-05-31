import gymnasium as gym
from gymnasium import spaces
import numpy as np
class TTCCalculator:

    @staticmethod
    def calculate(
        distance,
        relative_speed
    ):

        if relative_speed <= 0:
            return float("inf")

        return distance / relative_speed


class RiskQuantifier:

    def quantify(
        self,
        ttc,
        visibility
    ):

        score = 0

        # TTC 기반 위험도

        if ttc < 1:
            score += 50

        elif ttc < 2:
            score += 35

        elif ttc < 4:
            score += 20

        # Visibility 기반 위험도

        if visibility < 15:
            score += 30

        elif visibility < 30:
            score += 20

        elif visibility < 50:
            score += 10

        return score


class SaraEngine:

    def __init__(
        self,
        critical_threshold=1.0,
        dangerous_threshold=3.0
    ):

        self.critical_threshold = (
            critical_threshold
        )

        self.dangerous_threshold = (
            dangerous_threshold
        )

    def assess(
        self,
        ttc
    ):

        if ttc < self.critical_threshold:
            return "CRITICAL"

        if ttc < self.dangerous_threshold:
            return "DANGEROUS"

        return "SAFE"

class ControllabilityClassifier:

    def __init__(self, rl_model=None):
        self.rl_model = rl_model

    def classify(self, ttc, risk_score, visibility):

        # RL이 있으면 RL 사용
        if self.rl_model is not None:

            state = [ttc, risk_score, visibility, 0]

            action, _ = self.rl_model.predict(state)

            return ["C1", "C2", "C3"][action]

        # fallback = 기존 rule-based
        if (
            ttc < 1
            or risk_score >= 80
            or visibility < 15
        ):
            return "C3"

        if (
            ttc < 3
            or risk_score >= 50
            or visibility < 30
        ):
            return "C2"

        return "C1"

class ControllabilityEnv(gym.Env):

    def __init__(self):

        super().__init__()

        # ACTION: C1, C2, C3
        self.action_space = spaces.Discrete(3)

        # STATE: continuous (PPO 핵심)
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0]),
            high=np.array([100.0, 100.0, 100.0, 2.0]),
            dtype=np.float32
        )

        self.state = None
        self.step_count = 0
        self.max_steps = 200

    # -------------------
    def reset(self, seed=None, options=None):

        self.step_count = 0
        self.state = self._generate_state()

        return self.state, {}

    # -------------------
    def step(self, action):

        ttc, risk, vis, sara = self.state

        reward = self._reward(action, sara)

        next_state = self._generate_state()

        self.state = next_state
        self.step_count += 1

        done = self.step_count >= self.max_steps

        return next_state, reward, done, False, {}

    # -------------------
    def _generate_state(self):

        distance = np.random.uniform(5, 80)
        rel_speed = np.random.uniform(1, 30)
        visibility = np.random.uniform(5, 80)

        ttc = self._ttc(distance, rel_speed)
        risk = self._risk(ttc, visibility)
        sara = self._sara(ttc)

        return np.array([ttc, risk, visibility, sara], dtype=np.float32)

    # -------------------
    def _ttc(self, d, v):
        return 100.0 if v <= 0 else d / v

    def _risk(self, ttc, vis):
        score = 0
        if ttc < 1: score += 50
        elif ttc < 2: score += 35
        elif ttc < 4: score += 20

        if vis < 15: score += 30
        elif vis < 30: score += 20
        elif vis < 50: score += 10

        return score

    def _sara(self, ttc):
        if ttc < 1: return 2
        elif ttc < 3: return 1
        return 0

    # -------------------
    def _reward(self, action, sara):

        # 0=C1,1=C2,2=C3

        if sara == 2:
            return 10 if action == 2 else -10

        if sara == 1:
            return 8 if action == 1 else -6

        return 5 if action == 0 else -3