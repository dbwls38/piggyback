import airsim
import numpy as np

class LidarSensor:
    def __init__(self, client):
        self.client = client

    def get_point_cloud(self):
        lidar_data = self.client.getLidarData()

        points = np.array(
            lidar_data.point_cloud,
            dtype=np.float32
        )

        return points.reshape(-1, 3)