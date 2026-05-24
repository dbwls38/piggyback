import pandas as pd

class LogAnalyzer:
    def analyze(self, log_path):
        df = pd.read_csv(log_path)

        return {
            "avg_ttc": df["ttc"].mean(),
            "danger_count": len(df[df["ttc"] < 2])
        }