import json
import csv
import os
from datetime import datetime


class ReportWriter:

    def __init__(self):

        self.base_path = "reports/accuracy"

        # Create folder if not exists
        os.makedirs(self.base_path, exist_ok=True)

    def save_json(self, report):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = f"{self.base_path}/accuracy_report_{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:

            json.dump(report, f, indent=4)

        return file_path

    def save_csv(self, report):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = f"{self.base_path}/accuracy_report_{timestamp}.csv"

        with open(file_path, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                "Prompt",
                "Expected",
                "Response",
                "Similarity",
                "Correct"
            ])

            for r in report["results"]:

                writer.writerow([
                    r["prompt"],
                    r["expected"],
                    r["response"],
                    round(r["similarity"],3),
                    r["correct"]
                ])

        return file_path


    def save_hallucination_json(self, report):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        folder = "reports/hallucination"

        os.makedirs(folder, exist_ok=True)

        file_path = f"{folder}/hallucination_report_{timestamp}.json"

        with open(file_path,"w",encoding="utf-8") as f:

            json.dump(report,f,indent=4)

        return file_path


    def save_hallucination_csv(self, report):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        folder = "reports/hallucination"

        os.makedirs(folder, exist_ok=True)

        file_path = f"{folder}/hallucination_report_{timestamp}.csv"

        with open(file_path,"w",newline="",encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([

                "Prompt",
                "Expected",
                "Response",
                "Similarity",
                "Label",
                "Hallucinated"

            ])

            for r in report["results"]:

                writer.writerow([

                    r["prompt"],

                    r["expected"],

                    r["response"],

                    round(r["similarity"],3),

                    r["label"],

                    r["hallucinated"]

                ])

        return file_path