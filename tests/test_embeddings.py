import numpy as np
from src.rag_pipeline import RAGPipeline
import pytest

def test_embedding_dimension():
    # We mock the embedding generation or check the configured model
    rag = RAGPipeline()
    embedding_dim = rag.embeddings.client.get_sentence_embedding_dimension()
    assert embedding_dim == 384  # MiniLM-L6-v2 dimension

def test_embedding_type():
    rag = RAGPipeline()
    test_text = "Standardizing this text to vector."
    vector = rag.embeddings.embed_query(test_text)
    assert isinstance(vector, list)
    assert isinstance(vector[0], float)
