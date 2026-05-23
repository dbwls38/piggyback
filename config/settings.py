CARLA_HOST = "localhost"
CARLA_PORT = 2000

SAFE_TTC = 5.0
WARNING_TTC = 3.0
DANGER_TTC = 1.5

import yaml

class Settings:
    def __init__(self):

        with open(
            "config/hara_config.yaml",
            "r",
            encoding="utf-8"
        ) as file:

            self.config = yaml.safe_load(
                file
            )

    def get(self):
        return self.config