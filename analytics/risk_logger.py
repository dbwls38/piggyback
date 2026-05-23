import json
import os
from datetime import datetime

class RiskLogger:
    def __init__(self):
        self.log_dir = "logs/hara_logs"

        os.makedirs(
            self.log_dir,
            exist_ok=True
        )

    def save(
        self,
        scenario,
        sara_result,
        hara_result
    ):

        timestamp = (
            datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
        )

        filename = (
            f"{self.log_dir}/"
            f"risk_log_{timestamp}.json"
        )

        log_data = {

            "timestamp":
                timestamp,

            "scenario":
                scenario,

            "sara_result":
                sara_result,

            "hara_result":
                hara_result
        }

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                log_data,
                file,
                indent=4
            )

        print(
            f"[LOG SAVED] {filename}"
        )