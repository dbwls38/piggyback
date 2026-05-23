class ControllabilityMapper:
    def map(
        self,
        sara_controllability
    ):
        mapping = {

            "C1": "C1",

            "C2": "C2",

            "C3": "C3"
        }
        return mapping.get(
            sara_controllability,
            "C1"
        )