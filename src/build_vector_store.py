import os
import pandas as pd
import numpy as np
import logging
from typing import List, Dict

# NLP / AI Libraries
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_and_sample_data(input_path: str, target_sample_size: int = 15000) -> pd.DataFrame:
    """
    Loads the cleaned dataset and performs stratified sampling across product categories.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {input_path}")

    logger.info(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Ensure mandatory columns exist
    required_cols = ['Product', 'cleaned_narrative', 'Complaint ID']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    total_records = len(df)
    logger.info(f"Total records available: {total_records}")

    if total_records <= target_sample_size:
        logger.info("Dataset size is smaller than target sample size. Using full dataset.")
        return df

    # Stratified sampling
    logger.info(f"Performing stratified sampling for {target_sample_size} records...")
    # Some products might have very few samples, we handle them by merging or just accepting small strata
    # But for a simple stratified split:
    _, df_sampled = train_test_split(
        df, 
        test_size=target_sample_size, 
        stratify=df['Product'], 
        random_state=42
    )
    
    logger.info(f"Sampled dataset size: {len(df_sampled)}")
    return df_sampled

def chunk_complaints(df: pd.DataFrame, chunk_size: int = 500, chunk_overlap: int = 50) -> List[Document]:
    """
    Chunks complaint narratives and attaches metadata.
    """
    logger.info(f"Chunking narratives with size {chunk_size} and overlap {chunk_overlap}...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    documents = []
    
    for _, row in df.iterrows():
        narrative = str(row['cleaned_narrative'])
        chunks = text_splitter.split_text(narrative)
        
        # Base metadata from row
        # Map columns based on CFPB schema observed in complaints_sample
        metadata_base = {
            "complaint_id": row.get("Complaint ID", ""),
            "product_category": row.get("Product", ""),
            "product": row.get("Sub-product", ""),
            "issue": row.get("Issue", ""),
            "sub_issue": row.get("Sub-issue", ""),
            "company": row.get("Company", ""),
            "state": row.get("State", ""),
            "date_received": row.get("Date received", ""),
            "total_chunks": len(chunks)
        }

        for i, chunk in enumerate(chunks):
            metadata = metadata_base.copy()
            metadata["chunk_index"] = i
            
            doc = Document(page_content=chunk, metadata=metadata)
            documents.append(doc)

    logger.info(f"Total chunks created: {len(documents)}")
    return documents

def build_and_save_vector_store(documents: List[Document], model_name: str, save_path: str):
    """
    Generates embeddings and builds/persists the FAISS vector store.
    """
    logger.info(f"Initializing embedding model: {model_name}...")
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    logger.info("Generating embeddings and building FAISS index (this may take a few minutes)...")
    vector_store = FAISS.from_documents(documents, embeddings)

    logger.info(f"Saving vector store to {save_path}...")
    parent_dir = os.path.dirname(save_path)
    if parent_dir and not os.path.exists(parent_dir):
        logger.info(f"Creating parent directory: {parent_dir}")
        os.makedirs(parent_dir)
    
    vector_store.save_local(save_path)
    logger.info("Vector store persisted successfully.")

def main():
    # Configuration
    INPUT_PATH = "data/processed/filtered_complaints.csv"
    VECTOR_STORE_DIR = "vector_store"
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    TARGET_SAMPLE_SIZE = 15000
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

    try:
        # 1. Load and Sample
        df_sampled = load_and_sample_data(INPUT_PATH, TARGET_SAMPLE_SIZE)
        
        # 2. Chunk
        documents = chunk_complaints(df_sampled, CHUNK_SIZE, CHUNK_OVERLAP)
        
        # 3. Build and Persist
        build_and_save_vector_store(documents, MODEL_NAME, VECTOR_STORE_DIR)
        
        print(f"\nVector store build Complete!")
        print(f"Vector store saved at: {VECTOR_STORE_DIR}")
        
    except Exception as e:
        logger.error(f"Failed to build vector store: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
