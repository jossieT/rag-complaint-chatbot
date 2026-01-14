"""
RAG Pipeline Evaluation Script

This script evaluates the quality of the RAG system by:
1. Running representative business questions
2. Capturing answers and sources
3. Creating an evaluation table
4. Analyzing quality metrics
"""

import os
import json
import logging
from typing import List, Dict
from rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Define business questions for evaluation
BUSINESS_QUESTIONS = [
    "Why are customers unhappy with Credit Cards?",
    "What recurring issues appear in Money Transfers?",
    "What are the main complaints about Personal Loans?",
    "What problems do customers face with Savings Accounts?",
    "How do customers describe fraudulent transactions?",
    "What are common issues with credit card fees?",
    "Why do customers complain about loan approval processes?",
    "What are the main issues with account access?",
    "What problems do customers report with customer service?",
    "What are common complaints about billing and statements?"
]


def evaluate_rag_system(rag_pipeline: RAGPipeline, questions: List[str]) -> List[Dict]:
    """
    Evaluate the RAG system with a set of questions.
    
    Args:
        rag_pipeline: Initialized RAG pipeline
        questions: List of questions to evaluate
        
    Returns:
        List of evaluation results
    """
    results = []
    
    for i, question in enumerate(questions, 1):
        logger.info(f"Evaluating question {i}/{len(questions)}: {question}")
        
        # Get response from RAG system
        response = rag_pipeline.query(question)
        
        # Structure the result
        result = {
            "question": question,
            "answer": response["answer"],
            "sources": response["sources"],
            "num_sources": response["num_sources"]
        }
        
        results.append(result)
    
    return results


def generate_markdown_report(results: List[Dict], output_path: str):
    """
    Generate a markdown evaluation report.
    
    Args:
        results: Evaluation results
        output_path: Path to save the report
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Header
        f.write("# RAG Pipeline Evaluation Report\n\n")
        f.write("## Overview\n\n")
        f.write(f"This report evaluates the RAG system using {len(results)} representative business questions.\n\n")
        
        # Evaluation Table
        f.write("## Evaluation Results\n\n")
        f.write("| # | Question | Generated Answer | Quality Score | Comments |\n")
        f.write("|---|----------|-----------------|---------------|----------|\n")
        
        for i, result in enumerate(results, 1):
            question = result["question"]
            answer = result["answer"][:150] + "..." if len(result["answer"]) > 150 else result["answer"]
            answer = answer.replace("\n", " ").replace("|", "\\|")
            
            # Placeholder for manual quality scoring
            f.write(f"| {i} | {question} | {answer} | _/5 | |\n")
        
        f.write("\n")
        
        # Detailed Results
        f.write("## Detailed Results\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"### Question {i}: {result['question']}\n\n")
            
            f.write("**Generated Answer:**\n\n")
            f.write(f"{result['answer']}\n\n")
            
            f.write(f"**Number of Sources Retrieved:** {result['num_sources']}\n\n")
            
            if result['sources']:
                f.write("**Top Retrieved Sources:**\n\n")
                
                for j, source in enumerate(result['sources'], 1):
                    metadata = source['metadata']
                    f.write(f"**Source {j}:**\n")
                    f.write(f"- **Product Category:** {metadata.get('product_category', 'N/A')}\n")
                    f.write(f"- **Issue:** {metadata.get('issue', 'N/A')}\n")
                    f.write(f"- **Sub-Issue:** {metadata.get('sub_issue', 'N/A')}\n")
                    f.write(f"- **Complaint ID:** {metadata.get('complaint_id', 'N/A')}\n")
                    f.write(f"- **Date Received:** {metadata.get('date_received', 'N/A')}\n")
                    f.write(f"- **Similarity Score:** {source.get('similarity_score', 'N/A'):.4f}\n\n")
                    f.write(f"**Excerpt:**\n```\n{source['content'][:300]}...\n```\n\n")
            
            f.write("---\n\n")
        
        # Analysis Section
        f.write("## Analysis\n\n")
        f.write("### Strengths\n\n")
        f.write("- **Retrieval Quality:** [To be filled after manual review]\n")
        f.write("- **Answer Grounding:** [To be filled after manual review]\n")
        f.write("- **Source Citation:** [To be filled after manual review]\n\n")
        
        f.write("### Weaknesses\n\n")
        f.write("- **Coverage Gaps:** [To be filled after manual review]\n")
        f.write("- **Answer Quality:** [To be filled after manual review]\n")
        f.write("- **Retrieval Relevance:** [To be filled after manual review]\n\n")
        
        f.write("### Recommendations\n\n")
        f.write("1. [To be filled after manual review]\n")
        f.write("2. [To be filled after manual review]\n")
        f.write("3. [To be filled after manual review]\n\n")
        
        # Summary Statistics
        f.write("## Summary Statistics\n\n")
        
        total_sources = sum(r['num_sources'] for r in results)
        avg_sources = total_sources / len(results) if results else 0
        
        f.write(f"- **Total Questions Evaluated:** {len(results)}\n")
        f.write(f"- **Average Sources Retrieved per Question:** {avg_sources:.2f}\n")
        f.write(f"- **Questions with Sources:** {sum(1 for r in results if r['num_sources'] > 0)}\n")
        f.write(f"- **Questions without Sources:** {sum(1 for r in results if r['num_sources'] == 0)}\n\n")


def main():
    """Main evaluation workflow."""
    print("=" * 80)
    print("RAG Pipeline Evaluation")
    print("=" * 80)
    
    # Initialize RAG pipeline
    logger.info("Initializing RAG pipeline...")
    rag = RAGPipeline()
    
    # Run evaluation
    logger.info(f"Evaluating {len(BUSINESS_QUESTIONS)} business questions...")
    results = evaluate_rag_system(rag, BUSINESS_QUESTIONS)
    
    # Generate report
    output_path = "docs/evaluation_report.md"
    os.makedirs("docs", exist_ok=True)
    
    logger.info(f"Generating evaluation report at {output_path}...")
    generate_markdown_report(results, output_path)
    
    print("\n" + "=" * 80)
    print(f"Evaluation Complete!")
    print(f"Report saved to: {output_path}")
    print("=" * 80)
    
    # Print summary
    print("\nSummary:")
    print(f"- Questions evaluated: {len(results)}")
    print(f"- Questions with sources: {sum(1 for r in results if r['num_sources'] > 0)}")
    print(f"- Average sources per question: {sum(r['num_sources'] for r in results) / len(results):.2f}")


if __name__ == "__main__":
    main()
