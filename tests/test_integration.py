from src.rag_pipeline import RAGPipeline
import pytest

def test_full_rag_flow():
    """
    Integration test: Query -> Retrieval -> Generation
    Ensures all components work together.
    """
    rag = RAGPipeline()
    query = "What are common complaints about credit cards?"
    
    # 1. Test Query
    response = rag.query(query)
    
    # 2. Verify Output
    assert isinstance(response["answer"], str)
    assert len(response["answer"]) > 0
    assert response["num_sources"] > 0
    assert len(response["sources"]) > 0
    
    # Check if answer is not a generic error
    assert "An error occurred" not in response["answer"]
    
    # 3. Check source content
    for source in response["sources"]:
        assert "content" in source
        assert "metadata" in source
