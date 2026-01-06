import os
import sys
import pandas as pd

# Ensure src is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import process_dataset

def main():
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_data_path = os.path.join(base_dir, 'data', 'raw', 'complaints_sample.csv')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    output_path = os.path.join(processed_dir, 'filtered_complaints.csv')

    # Ensure processed directory exists
    if not os.path.exists(processed_dir):
        print(f"Creating directory: {processed_dir}")
        os.makedirs(processed_dir)

    # Check if raw data exists
    if not os.path.exists(raw_data_path):
        print(f"Error: Raw data file not found at {raw_data_path}")
        return

    print("Starting dataset processing...")
    try:
        # distinct chunk_size can be adjusted based on memory availability
        processed_count = process_dataset(raw_data_path, output_path, chunk_size=100000)
        print(f"Successfully processed {processed_count} complaints.")
        print(f"Output saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
