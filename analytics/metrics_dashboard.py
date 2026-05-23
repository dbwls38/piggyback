class MetricsDashboard:

    def display(
        self,
        sara_result,
        hara_result
    ):

        print()

        print("========== DASHBOARD ==========")

        print(
            f"TTC: "
            f"{sara_result['ttc']:.2f}"
        )

        print(
            f"Controllability: "
            f"{sara_result['controllability']}"
        )

        print(
            f"Severity: "
            f"{hara_result['severity']}"
        )

        print(
            f"Exposure: "
            f"{hara_result['exposure']}"
        )

        print(
            f"ASIL: "
            f"{hara_result['asil']}"
        )

        print(
            "================================"
        )