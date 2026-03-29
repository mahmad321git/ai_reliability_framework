from typing import List, Dict
from llm.llm_client import ask_llm
from sentence_transformers import SentenceTransformer, util
from reports.report_writer import ReportWriter

class HallucinationEvaluator:
    def __init__(self, hallucination_threshold: float = 0.45, grounded_threshold: float = 0.70):

        """
        Detect hallucinations in LLM responses using semantic similarity.

        Hallucination logic:

        High similarity → grounded response
        Medium similarity → partial grounding
        Low similarity → hallucination
        """
        self.hallucination_threshold = hallucination_threshold
        self.grounded_threshold = grounded_threshold
        self.embed_model =  SentenceTransformer('all-MiniLM-L6-v2')

    def detect_hallucination(self, expected: str, response: str) -> Dict:
        expected_emb = self.embed_model.encode(
            expected, convert_to_tensor=True
        )
        response_emb = self.embed_model.encode(
            response, convert_to_tensor=True
        )
        similarity = util.pytorch_cos_sim(
            expected_emb, response_emb
        ).item()

        if similarity < self.hallucination_threshold:
            label = "Hallucinated"
            hallucinated =  True
        elif similarity < self.grounded_threshold:
            label = "Partially grounded"
            hallucinated = False
        else:
            label = "Grounded"
            hallucinated = False

        return {
            "similarity": similarity,
            "label": label,
            "hallucinated": hallucinated
        }
    
    def evaluate_dataset(self, dataset: List[Dict[str, str]]) -> Dict:
        results = []

        hallucination_count = 0

        for case in dataset:

            prompt = case["prompt"]

            expected = case["expected"]

            response = ask_llm(prompt)

            result = self.detect_hallucination(
                expected,
                response
            )

            if result is None:
                raise RuntimeError(f"detect_hallucination returned None for prompt: {prompt}")

            results.append({
                "prompt": prompt,
                "expected": expected,
                "response": response,
                "similarity": result["similarity"],
                "label": result["label"],
                "hallucinated": result["hallucinated"]
            })

            if result["hallucinated"]:
                hallucination_count += 1

        total = len(dataset)

        hallucination_rate = (

            hallucination_count / total

            if total else 0

        )

        return {

            "hallucination_rate": hallucination_rate,

            "total_cases": total,

            "hallucination_count": hallucination_count,

            "results": results
        }



