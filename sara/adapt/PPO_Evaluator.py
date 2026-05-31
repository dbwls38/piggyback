import numpy as np

class RLEvaluator:

    def __init__(self, env, model):
        self.env = env
        self.model = model

        self.rewards = []
        self.violations = 0
        self.total_steps = 0

    # -------------------------
    # RUN EPISODE
    # -------------------------
    def run_episode(self):

        obs, _ = self.env.reset()
        done = False

        episode_reward = 0

        while not done:

            action, _ = self.model.predict(obs)

            next_obs, reward, done, _, _ = self.env.step(action)

            episode_reward += reward

            # safety violation tracking
            self._check_violation(obs, action)

            obs = next_obs
            self.total_steps += 1

        self.rewards.append(episode_reward)

    # -------------------------
    # SAFETY VIOLATION
    # -------------------------
    def _check_violation(self, state, action):

        ttc, risk, visibility, sara = state

        # CRITICAL 상황에서 C3 안 하면 violation
        if sara == 2 and action != 2:
            self.violations += 1

        # DANGEROUS 상황에서 C2 안 하면 violation
        if sara == 1 and action != 1:
            self.violations += 1

        # SAFE인데 과도하게 C3 선택하면 inefficiency violation
        if sara == 0 and action == 2:
            self.violations += 1

    # -------------------------
    # METRICS
    # -------------------------
    def compute_metrics(self):

        avg_reward = np.mean(self.rewards)

        violation_rate = (
            self.violations / max(1, self.total_steps)
        )

        return {
            "avg_reward": avg_reward,
            "safety_violation_rate": violation_rate,
            "episodes": len(self.rewards)
        }

