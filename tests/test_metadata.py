from src.rag_pipeline import RAGPipeline
import pytest

def test_metadata_fields():
    rag = RAGPipeline()
    results = rag.retrieve_relevant_complaints("credit card", k=1)
    if results:
        metadata = results[0]["metadata"]
        # Basic fields we expect from our schema
        assert "product_category" in metadata
        assert "issue" in metadata
        assert "complaint_id" in metadata

def test_context_formatting_with_metadata():
    rag = RAGPipeline()
    mock_docs = [
        {"content": "Text 1", "metadata": {"product_category": "A", "issue": "X"}},
        {"content": "Text 2", "metadata": {"product_category": "B", "issue": "Y"}}
    ]
    context = rag._format_context(mock_docs)
    assert "Product: A" in context
    assert "Issue: X" in context
    assert "Product: B" in context
