from utils.file_loader import load_dataset
from llm.llm_client import ask_llm
from evaluation.accuracy_evaluator import AccuracyEvaluator
from reports.report_writer import ReportWriter


def test_llm_on_qa_dataset():

    # Step 1: Load dataset
    dataset = load_dataset("datasets/qa_datasets.json")

    # Step 2: Take first test case
    test_case = dataset[1]

    prompt = test_case["prompt"]
    expected = test_case["expected"]

    # Step 3: Send to LLM
    response = ask_llm(prompt)

    # Step 4: Print results
    print("\nPrompt:", prompt)
    print("Expected:", expected)
    print("Response:", response)

    # Step 3: Initialize evaluator with vectorized semantic similarity
    evaluator = AccuracyEvaluator(
        use_semantic=True
    )
    
    # Step 5: Evaluate first N samples (or full dataset)
    report = evaluator.evaluate_dataset(dataset[:5])

    writer = ReportWriter()

    json_path = writer.save_json(report)

    csv_path = writer.save_csv(report)

    print("Reports saved:")
    print(json_path)
    print(csv_path)

    # Step 6: Print results
    print("Overall Accuracy:", report['accuracy'])
    for res in report['results']:
        print(f"Prompt: {res['prompt']}")
        print(f"Expected: {res['expected']}")
        print(f"Response: {res['response']}")
        print(f"Similarity: {res['similarity']:.3f}")
        print(f"Correct: {res['correct']}")
        print("-" * 50)




if __name__ == "__main__":
    test_llm_on_qa_dataset()