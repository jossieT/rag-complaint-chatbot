from src.rag_pipeline import RAGPipeline
import pytest

def test_retrieval_structure():
    rag = RAGPipeline()
    results = rag.retrieve_relevant_complaints("bank transfer", k=2)
    assert isinstance(results, list)
    if results:
        assert "content" in results[0]
        assert "metadata" in results[0]
        assert "similarity_score" in results[0]
        assert len(results) <= 2

def test_retrieval_empty_query():
    rag = RAGPipeline()
    results = rag.retrieve_relevant_complaints("", k=1)
    # Depending on FAISS, an empty query might still return something or error
    # Our implementation should handle it gracefully
    assert isinstance(results, list)
