from utils.file_loader import load_dataset
from llm.llm_client import ask_llm

if __name__ == "__main__":
    qa_data = load_dataset("datasets/qa_datasets.json")
    print(f"QA Data set loaded {qa_data}")

    hallucination_data = load_dataset("datasets/hallucination_dataset.json")
    print(f"hallucination Data set loaded {qa_data}")

