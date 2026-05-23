from hara.iso26262_table import (
    ASIL_TABLE
)


class ASILClassifier:

    def classify(
        self,
        severity,
        exposure,
        controllability
    ):

        key = (
            severity,
            exposure,
            controllability
        )

        asil = (
            ASIL_TABLE.get(
                key,
                "QM"
            )
        )

        return asil