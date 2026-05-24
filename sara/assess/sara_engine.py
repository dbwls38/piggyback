class SaraEngine:

    def __init__(self,
                 ttc_threshold=3.0):

        self.ttc_threshold = ttc_threshold

    def assess(self, ttc):

        if ttc < 1.0:
            return "CRITICAL"
        

        if ttc < self.ttc_threshold:
            return "DANGEROUS"

        return "SAFE"