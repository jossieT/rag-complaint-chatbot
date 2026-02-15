import pytest
from langchain_core.documents import Document
import numpy as np
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_text():
    return "This is a sample consumer complaint about reaching out to the bank regarding unauthorized charges. The bank did not resolve the issue quickly."

@pytest.fixture
def mock_documents():
    return [
        Document(
            page_content="I had an unauthorized charge on my credit card.",
            metadata={"product_category": "Credit Card", "issue": "Unauthorized charge", "id": "1"}
        ),
        Document(
            page_content="My personal loan application was rejected without clear reason.",
            metadata={"product_category": "Personal Loan", "issue": "Loan application", "id": "2"}
        )
    ]

@pytest.fixture
def mock_embedding():
    return np.random.rand(384).astype('float32').tolist()
