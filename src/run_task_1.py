import os
import sys
import pandas as pd

# Add current directory to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from preprocessing import process_dataset
from eda_utils import perform_eda

def main():
    raw_path = 'data/raw/complaints_sample.csv'
    processed_path = 'data/processed/filtered_complaints.csv'
    
    if not os.path.exists('data/processed'):
        os.makedirs('data/processed')
    
    print("--- Starting EDA on Raw Data ---")
    df_raw = pd.read_csv(raw_path)
    # Redirect output dir for images
    if not os.path.exists('docs/images'):
        os.makedirs('docs/images')
    
    # Run EDA
    perform_eda(df_raw, output_dir='docs/images')
    
    print("\n--- Processing Dataset ---")
    processed_count = process_dataset(raw_path, processed_path)
    print(f"Original size: {len(df_raw)}")
    print(f"Filtered size: {processed_count}")
    
    print("\n--- Sample of Processed Data ---")
    df_processed_sample = pd.read_csv(processed_path, nrows=5)
    print(df_processed_sample[['Product', 'cleaned_narrative']].head())
    
    print("\nTask 1 completed successfully.")

if __name__ == "__main__":
    main()
