class HARAEngine:

    def evaluate(self, scenario):

        if scenario["pedestrian"]:
            return {
                "S": 2,
                "E": 3,
                "C": 2,
                "ASIL": "B"
            }

        return {
            "S": 1,
            "E": 2,
            "C": 1,
            "ASIL": "A"
        }