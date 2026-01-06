import os
import sys
import pandas as pd

print("Imports successful")
raw_path = 'data/raw/complaints_sample.csv'
if os.path.exists(raw_path):
    print(f"Found {raw_path}")
    df = pd.read_csv(raw_path)
    print(f"Loaded {len(df)} rows")
    print(df.head())
else:
    print(f"File {raw_path} NOT found")
