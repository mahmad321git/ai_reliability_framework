from typing import List, Dict
from llm.llm_client import ask_llm

from sentence_transformers import SentenceTransformer, util

class AccuracyEvaluator:
    def __init__(self, use_semantic: bool = False):
        self.use_semantic = use_semantic

        if use_semantic:
            self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')

    def evaluate_dataset(self, dataset: List[Dict[str, str]], similarity_threshold: float = 0.5) -> Dict:

        results = []
        correct_count = 0

        for case in dataset:
            prompt = case['prompt']
            expected = case['expected']

            response = ask_llm(prompt)

            if self.use_semantic:
                # Compute semantic similarity
                expected_emb = self.embed_model.encode(expected, convert_to_tensor=True)
                response_emb = self.embed_model.encode(response, convert_to_tensor=True)
                similarity = util.pytorch_cos_sim(expected_emb, response_emb).item()
                is_correct = similarity >= similarity_threshold
            else:
                # Exact string match
                is_correct = response.strip().lower() == expected.strip().lower()

            results.append({
                'prompt': prompt,
                'expected': expected,
                'response': response,
                'similarity': similarity,
                'correct': is_correct
            })

            if is_correct:
                correct_count += 1

        accuracy = correct_count / len(dataset) if dataset else 0

        return {
            'accuracy': accuracy,
            'results': results
        }