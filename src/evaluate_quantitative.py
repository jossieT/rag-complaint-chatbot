"""
Quantitative Evaluation Script for RAG Pipeline

This script implements light quantitative metrics to assess the quality
of the RAG system, focusing on:
- Retrieval Accuracy (Context Relevance)
- Answer Relevancy (Question-Answer Alignment)
- Faithfulness (Grounding in Context)
"""

import os
import yaml
import logging
import pandas as pd
from src.rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuantitativeEvaluator:
    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag = rag_pipeline
        self.test_questions = [
            "Why are customers unhappy with Credit Cards?",
            "What recurring issues appear in Money Transfers?",
            "What are the main complaints about Personal Loans?",
            "What problems do customers face with Savings Accounts?",
            "How do customers describe fraudulent transactions?"
        ]

    def _calculate_overlap_score(self, question: str, answer: str) -> float:
        """Simple keyword overlap as a proxy for answer relevancy."""
        q_words = set(question.lower().split())
        a_words = set(answer.lower().split())
        if not q_words: return 0.0
        overlap = q_words.intersection(a_words)
        return len(overlap) / len(q_words)

    def _check_grounding(self, answer: str, context: str) -> float:
        """Lightweight check if answer keywords appear in context (Faithfulness)."""
        if "don't have enough information" in answer.lower() or "not find any relevant" in answer.lower():
            return 1.0  # Safe answer is faithful
            
        a_words = set(w for w in answer.lower().split() if len(w) > 3)
        if not a_words: return 1.0
        
        found = sum(1 for w in a_words if w in context.lower())
        return found / len(a_words)

    def evaluate(self):
        logger.info("Starting Quantitative Evaluation...")
        results = []
        
        for q in self.test_questions:
            response = self.rag.generate_answer(q)
            answer = response['answer']
            sources = response['sources']
            context = " ".join([s['content'] for s in sources])
            
            relevancy = self._calculate_overlap_score(q, answer)
            faithfulness = self._check_grounding(answer, context)
            
            results.append({
                "question": q,
                "relevancy_score": round(relevancy, 2),
                "faithfulness_score": round(faithfulness, 2),
                "num_sources": len(sources)
            })
            
        df = pd.DataFrame(results)
        
        # Save results
        output_dir = "docs"
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, "quantitative_metrics.csv")
        df.to_csv(csv_path, index=False)
        
        logger.info(f"Evaluation complete. Metrics saved to {csv_path}")
        
        # Print summary
        print("\n=== Quantitative Evaluation Summary ===")
        print(df.drop(columns=['question']).mean())
        print("========================================\n")

if __name__ == "__main__":
    try:
        pipeline = RAGPipeline()
        evaluator = QuantitativeEvaluator(pipeline)
        evaluator.evaluate()
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
