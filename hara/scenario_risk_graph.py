class ScenarioRiskGraph:

    def build_graph(
        self,
        scenario,
        sara_result,
        hara_result
    ):

        graph = {

            "Weather":
                scenario[
                    "weather"
                ][
                    "condition"
                ],

            "Pedestrian":
                scenario[
                    "pedestrian"
                ][
                    "behavior"
                ],

            "TTC":
                sara_result[
                    "ttc"
                ],

            "Controllability":
                sara_result[
                    "controllability"
                ],

            "ASIL":
                hara_result[
                    "asil"
                ]
        }

        return graph

    def visualize(
        self,
        graph
    ):

        print()

        print(
            "===== RISK GRAPH ====="
        )

        for key, value in graph.items():

            print(
                f"{key} -> {value}"
            )