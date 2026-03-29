from utils.file_loader import load_dataset

if __name__ == "main":
    qa_data = load_dataset("datasets/qa_datasets.json")
    print(f"QA Data set loaded {qa_data}")

    hallucination_data = load_dataset("datasets/hallucination_datasets.json")
    print(f"hallucination Data set loaded {qa_data}")

