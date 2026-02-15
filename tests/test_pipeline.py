from src.rag_pipeline import RAGPipeline
import pytest

def test_pipeline_response_keys():
    rag = RAGPipeline()
    response = rag.query("Test question?")
    expected_keys = {"answer", "sources", "query", "num_sources"}
    assert all(key in response for key in expected_keys)

def test_pipeline_invalid_input():
    rag = RAGPipeline()
    response = rag.query(None)
    assert "Please provide a valid question" in response["answer"]
    assert response["sources"] == []
