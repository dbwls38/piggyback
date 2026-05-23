import csv
import os
from datetime import datetime

class ScenarioRecorder:
    def __init__(self):

        self.output_dir = (
            "logs/scenario_logs"
        )

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

        self.file_path = (
            f"{self.output_dir}/"
            f"scenario_records.csv"
        )

        if not os.path.exists(
            self.file_path
        ):

            with open(
                self.file_path,
                "w",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "timestamp",
                    "scenario",
                    "weather",
                    "corner_case",
                    "vehicle_speed",
                    "pedestrian_behavior"
                ])

    def record(
        self,
        scenario
    ):

        with open(
            self.file_path,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([

                datetime.now(),

                scenario[
                    "scenario_type"
                ],

                scenario[
                    "weather"
                ][
                    "condition"
                ],

                scenario[
                    "corner_case"
                ][
                    "type"
                ],

                scenario[
                    "traffic"
                ][
                    "average_speed"
                ],

                scenario[
                    "pedestrian"
                ][
                    "behavior"
                ]
            ])

        print(
            "[SCENARIO RECORDED]"
        )