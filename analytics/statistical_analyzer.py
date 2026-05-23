import pandas as pd

class StatisticalAnalyzer:
    def analyze(
        self,
        csv_path
    ):

        df = pd.read_csv(csv_path)

        print()

        print("===== STATISTICS =====")

        print(
            f"Total Scenarios: "
            f"{len(df)}"
        )

        print()

        print(
            "Scenario Distribution:"
        )

        print(
            df[
                "scenario"
            ].value_counts()
        )

        print()

        print(
            "Weather Distribution:"
        )

        print(
            df[
                "weather"
            ].value_counts()
        )

        print()

        print(
            "Corner Case Distribution:"
        )

        print(
            df[
                "corner_case"
            ].value_counts()
        )

