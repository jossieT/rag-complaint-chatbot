from src.build_vector_store import chunk_complaints
import pandas as pd

def test_chunking_output_type():
    df = pd.DataFrame({
        'cleaned_narrative': ["This is a test complaint." * 10],
        'Product': ["Credit card"],
        'Complaint ID': [1]
    })
    chunks = chunk_complaints(df, chunk_size=20, chunk_overlap=5)
    assert isinstance(chunks, list)
    if chunks:
        from langchain_core.documents import Document
        assert isinstance(chunks[0], Document)

def test_chunking_metadata_persistence():
    df = pd.DataFrame({
        'cleaned_narrative': ["Test " * 50],
        'Product': ["Checking or savings account"],
        'Complaint ID': ["12345"]
    })
    chunks = chunk_complaints(df, chunk_size=100)
    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk.metadata['product_category'] == "Checking or savings account"
        assert chunk.metadata['complaint_id'] == "12345"
