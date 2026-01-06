import pandas as pd
import re
import string

def clean_narrative(text):
    """
    Cleans the complaint narrative text.
    - Lowercases the text
    - Removes special characters
    - Removes specific boilerplate phrases
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove boilerplate phrases
    boilerplate_phrases = [
        "i am writing to file a complaint",
        "to whom it may concern",
        "i am writing to you today",
        "please investigate this matter"
    ]
    for phrase in boilerplate_phrases:
        text = text.replace(phrase, "")
    
    # 3. Remove special characters (keep alphanumeric and basic punctuation)
    # We might want to keep some punctuation for semantic search, but the prompt says 
    # "Remove special characters". I'll remove non-alphanumeric except spaces.
    # Actually, often for RAG keeping punctuation is better for the embedding model.
    # But I will follow the instruction: "Remove special characters"
    # Let's keep spaces and basic punctuation for now, but remove unusual ones.
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    
    # 4. Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def filter_complaints(df):
    """
    Filters the dataset to include ONLY:
    - Credit Cards
    - Personal Loans
    - Savings Accounts
    - Money Transfers
    Removes complaints without narratives.
    """
    # Define mapping or filter substrings
    # CFPB products often have longer names
    target_products = [
        'Credit card', 
        'Credit card or prepaid card',
        'Checking or savings account',
        'Money transfer',
        'Money transfer, virtual currency, or money service',
        'Payday loan, title loan, or personal loan',
        'Personal loan'
    ]
    
    # Filter by product (case insensitive check or exact match)
    mask = df['Product'].str.contains('|'.join(target_products), case=False, na=False)
    filtered_df = df[mask].copy()
    
    # Remove complaints without narratives
    # Column name is usually 'Consumer complaint narrative'
    narrative_col = 'Consumer complaint narrative'
    if narrative_col in filtered_df.columns:
        filtered_df = filtered_df[filtered_df[narrative_col].notna()]
        filtered_df = filtered_df[filtered_df[narrative_col].str.strip() != ""]
    
    return filtered_df

def process_dataset(input_path, output_path, chunk_size=50000):
    """
    Full pipeline: Load, filter, clean, save using chunking for large files.
    """
    import os
    
    # Remove existing output file if it exists to start fresh
    if os.path.exists(output_path):
        os.remove(output_path)
    
    narrative_col = 'Consumer complaint narrative'
    first_chunk = True
    processed_count = 0
    total_count = 0

    print(f"Processing {input_path} in chunks of {chunk_size}...")

    # Read the dataset in chunks
    for chunk in pd.read_csv(input_path, chunksize=chunk_size, low_memory=False):
        total_count += len(chunk)
        
        # 1. Filter chunk
        df_filtered = filter_complaints(chunk)
        
        if not df_filtered.empty:
            # 2. Clean narratives
            if narrative_col in df_filtered.columns:
                df_filtered['cleaned_narrative'] = df_filtered[narrative_col].apply(clean_narrative)
            
            # 3. Save chunk
            df_filtered.to_csv(output_path, mode='a', index=False, header=first_chunk)
            
            processed_count += len(df_filtered)
            first_chunk = False
            
        print(f"Processed {total_count} rows... (Filtered to {processed_count} so far)", end='\r')

    print(f"\nProcessing complete. Final dataset size: {processed_count}")
    return processed_count
