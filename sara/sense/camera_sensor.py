import airsim
import numpy as np
import cv2

class CameraSensor:
    def __init__(self, client):
        self.client = client

    def capture(self):
        responses = self.client.simGetImages([
            airsim.ImageRequest(
                "0",
                airsim.ImageType.Scene,
                False,
                False
            )
        ])

        img1d = np.frombuffer(
            responses[0].image_data_uint8,
            dtype=np.uint8
        )

        img_rgb = img1d.reshape(
            responses[0].height,
            responses[0].width,
            3
        )

        return img_rgb