from evaluation.hallucination_checker import HallucinationEvaluator
from llm.llm_client import ask_llm
from utils.file_loader import load_dataset
from reports.report_writer import ReportWriter

dataset = load_dataset(
    "datasets/hallucination_dataset.json"
)

evaluator = HallucinationEvaluator()

report = evaluator.evaluate_dataset(
    dataset[:5]
)

writer = ReportWriter()

json_path = writer.save_hallucination_json(report)

csv_path = writer.save_hallucination_csv(report)

print("Hallucination rate:",

report["hallucination_rate"])

print("Reports saved:")

print(json_path)

print(csv_path)

print(report["hallucination_rate"])

for r in report["results"]:

    print(r["label"], r["similarity"])

