from sara.sense.radar_sensor import (
    RadarSensor
)

from sara.sense.object_detector import (
    ObjectDetector
)

from sara.assess.sara_engine import (
    SaraEngine
)

from sara.react.vehicle_controller import (
    VehicleController
)


radar = RadarSensor()

detector = ObjectDetector()

engine = SaraEngine()

controller = VehicleController()


radar_objects = radar.scan()

detected_objects = (
    detector.detect(
        radar_objects
    )
)

vehicle = {

    "speed": 72
}


for obj in detected_objects:

    result = engine.evaluate(
        obj,
        visibility=18
    )

    print()

    print("===== SARA RESULT =====")

    print(result)

    controller.react(
        result,
        vehicle
    )