from hara.asil_classifier import (
    ASILClassifier
)


def test_asil_classifier():

    classifier = (
        ASILClassifier()
    )

    asil = classifier.classify(
        "S3",
        "E4",
        "C3"
    )

    print()

    print(
        "===== ASIL TEST ====="
    )

    print(
        f"ASIL: {asil}"
    )

    assert asil == "ASIL-D"