class CollisionPredictor:
    def predict(self, ttc):
        if ttc < 1.5:
            return 0.95

        if ttc < 3:
            return 0.60

        return 0.10