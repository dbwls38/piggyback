class SafetyScore:
    def calculate(self, ttc, collision_probability):
        score = 100

        score -= collision_probability * 50

        if ttc < 2:
            score -= 30

        return max(score, 0)