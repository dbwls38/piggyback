import numpy as np
from stable_baselines3 import PPO
import gymnasium as gym
from gymnasium import spaces


# ======================================================
# ENVIRONMENT (HARA + RL State)
# ======================================================
class ControllabilityEnv(gym.Env):

    def __init__(self):
        super().__init__()

        self.action_space = spaces.Discrete(3)

        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0]),
            high=np.array([100.0, 100.0, 100.0, 2.0]),
            dtype=np.float32
        )

        self.state = None
        self.step_count = 0
        self.max_steps = 50

        self.violations = 0
        self.total_steps = 0
        self.episode_rewards = []

    def reset(self, seed=None, options=None):

        self.step_count = 0
        self.state = self._generate_state()

        return self.state, {}

    def step(self, action):

        ttc, risk, vis, sara = self.state

        reward = self._reward(action, sara)

        next_state = self._generate_state()

        self._check_violation(action, sara)

        self.state = next_state
        self.step_count += 1
        self.total_steps += 1

        done = self.step_count >= self.max_steps

        return next_state, reward, done, False, {}

    # -------------------------
    # STATE GENERATION
    # -------------------------
    def _generate_state(self):

        distance = np.random.uniform(5, 80)
        rel_speed = np.random.uniform(1, 30)
        visibility = np.random.uniform(5, 80)

        ttc = self._ttc(distance, rel_speed)
        risk = self._risk(ttc, visibility)
        sara = self._sara(ttc)

        return np.array([ttc, risk, visibility, sara], dtype=np.float32)

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
        if ttc < 1:
            return 2  # CRITICAL
        elif ttc < 3:
            return 1  # DANGEROUS
        return 0

    # -------------------------
    # REWARD FUNCTION (HARA)
    # -------------------------
    def _reward(self, action, sara):

        if sara == 2:
            return 10 if action == 2 else -10

        if sara == 1:
            return 8 if action == 1 else -6

        return 5 if action == 0 else -3

    # -------------------------
    # SAFETY VIOLATION
    # -------------------------
    def _check_violation(self, action, sara):

        if sara == 2 and action != 2:
            self.violations += 1

        if sara == 1 and action != 1:
            self.violations += 1

        if sara == 0 and action == 2:
            self.violations += 1


# ======================================================
# ASIL CONSISTENCY
# ======================================================
def asil_consistency(env, model, episodes=50):

    correct = 0
    total = 0

    for _ in range(episodes):

        obs, _ = env.reset()
        done = False

        while not done:

            action, _ = model.predict(obs)

            ttc, risk, visibility, sara = obs

            expected = {
                2: 2,
                1: 1,
                0: 0
            }[int(sara)]

            if int(action) == expected:
                correct += 1

            total += 1

            obs, _, done, _, _ = env.step(action)

    return correct / max(1, total)


# ======================================================
# MAIN EVALUATION
# ======================================================
class RLEvaluator:

    def __init__(self, env, model):
        self.env = env
        self.model = model
        self.rewards = []

    def run_episode(self):

        obs, _ = self.env.reset()
        done = False

        ep_reward = 0

        while not done:

            action, _ = self.model.predict(obs)

            obs, reward, done, _, _ = self.env.step(action)

            ep_reward += reward

        self.rewards.append(ep_reward)

    def compute_metrics(self):

        return {
            "avg_reward": np.mean(self.rewards),
            "safety_violation_rate": self.env.violations / max(1, self.env.total_steps),
            "episodes": len(self.rewards)
        }


# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":

    env = ControllabilityEnv()
    model = PPO.load("hara_controllability_ppo")

    evaluator = RLEvaluator(env, model)

    for _ in range(50):
        evaluator.run_episode()

    metrics = evaluator.compute_metrics()
    asil_score = asil_consistency(env, model)

    print("===== RL SAFETY REPORT =====")
    print(f"Avg Reward: {metrics['avg_reward']:.2f}")
    print(f"Violation Rate: {metrics['safety_violation_rate']:.4f}")
    print(f"ASIL Consistency: {asil_score:.4f}")
    print(f"Episodes: {metrics['episodes']}")