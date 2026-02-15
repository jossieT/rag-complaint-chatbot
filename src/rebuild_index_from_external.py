import os
import pandas as pd
import numpy as np
import logging
import argparse
import pyarrow.parquet as pq
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ingest_from_parquet(
    parquet_path: str, 
    embedding_model_name: str,
    output_vector_store: str,
    text_column: str = "document",
    embedding_column: str = "element",
    batch_size: int = 50000
):
    """
    Ingests pre-computed embeddings and text from a parquet file into a FAISS index using memory-efficient batching.
    """
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Parquet file not found at {parquet_path}")

    logger.info(f"Initializing batch processing for {parquet_path}...")
    pf = pq.ParquetFile(parquet_path)
    
    logger.info(f"Schema columns: {pf.schema.names}")
    
    embeddings_wrapper = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_store = None
    total_processed = 0

    # Iterate through row groups/batches to save memory
    for batch in pf.iter_batches(batch_size=batch_size):
        df_batch = batch.to_pandas()
        logger.info(f"Processing batch of {len(df_batch)} records...")
        
        # 1. Prepare Content and Embeddings
        embeddings_list = df_batch[embedding_column].tolist()
        text_list = df_batch[text_column].tolist()
        
        # Ensure embeddings are float32
        embeddings_matrix = np.array(embeddings_list).astype('float32')
        
        # 2. Prepare Metadata
        # If metadata is a nested struct, it might be a dict in pandas. 
        # Extract it and merge with any top-level metadata columns if they exist.
        metadatas = []
        for idx, row in df_batch.iterrows():
            meta = {}
            # If 'metadata' column exists as a dict/struct
            if 'metadata' in row and isinstance(row['metadata'], dict):
                meta.update(row['metadata'])
            
            # Add any other potential metadata columns (excluding the main ones)
            for col in df_batch.columns:
                if col not in [embedding_column, text_column, 'metadata']:
                    meta[col] = row[col]
            metadatas.append(meta)
        
        # 3. Add to FAISS
        text_embedding_pairs = list(zip(text_list, embeddings_matrix))
        
        if vector_store is None:
            logger.info(f"Initializing FAISS index with first batch of {len(df_batch)} records...")
            vector_store = FAISS.from_embeddings(
                text_embeddings=text_embedding_pairs,
                embedding=embeddings_wrapper,
                metadatas=metadatas
            )
        else:
            logger.info(f"Adding {len(df_batch)} records to existing index...")
            vector_store.add_embeddings(
                text_embeddings=text_embedding_pairs,
                metadatas=metadatas
            )
        
        total_processed += len(df_batch)
        logger.info(f"Total processed: {total_processed}")

    # 4. Save Index
    if vector_store:
        logger.info(f"Saving new vector store to {output_vector_store}...")
        if not os.path.exists(output_vector_store):
            os.makedirs(output_vector_store)
        
        vector_store.save_local(output_vector_store)
        logger.info(f"Successfully rebuilt FAISS index with {total_processed} records.")
    else:
        logger.warning("No data found to ingest.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rebuild FAISS index from parquet embeddings using batching.")
    parser.add_argument("--input", default="data/complaint_embeddings.parquet", help="Path to parquet file")
    parser.add_argument("--output", default="vector_store", help="Path to save FAISS index")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2", help="Embedding model name")
    parser.add_argument("--text_col", default="document", help="Column name for text chunks")
    parser.add_argument("--emb_col", default="embedding", help="Column name for embeddings")
    parser.add_argument("--batch_size", type=int, default=50000, help="Batch size for processing")
    
    args = parser.parse_args()
    
    try:
        ingest_from_parquet(
            parquet_path=args.input,
            embedding_model_name=args.model,
            output_vector_store=args.output,
            text_column=args.text_col,
            embedding_column=args.emb_col,
            batch_size=args.batch_size
        )
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
