import pandas as pd
import requests

url = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?size=1000&format=csv"
output_path = "data/raw/complaints_sample.csv"

print(f"Downloading data from {url}...")
try:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(response.content)
    print(f"Data saved to {output_path}")
    
    # Verify the file
    df = pd.read_csv(output_path)
    print(f"Successfully loaded {len(df)} rows.")
    print("Columns:", df.columns.tolist())
except Exception as e:
    print(f"Error: {e}")
