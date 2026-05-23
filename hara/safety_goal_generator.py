class SafetyGoalGenerator:

    def generate(
        self,
        hara_result
    ):

        asil = (
            hara_result[
                "asil"
            ]
        )

        controllability = (
            hara_result[
                "controllability"
            ]
        )

        if asil == "ASIL-D":

            return {

                "goal":
                    "Prevent pedestrian collision "
                    "during right-turn scenarios.",

                "requirement":
                    "Emergency braking must activate "
                    "within 300ms.",

                "controllability":
                    controllability
            }

        if asil == "ASIL-C":

            return {

                "goal":
                    "Reduce collision probability.",

                "requirement":
                    "Driver warning required.",

                "controllability":
                    controllability
            }

        return {

            "goal":
                "Maintain safe driving.",

            "requirement":
                "Standard monitoring.",

            "controllability":
                controllability
        }