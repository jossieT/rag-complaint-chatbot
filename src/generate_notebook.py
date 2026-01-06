import nbformat as nbf

nb = nbf.v4.new_notebook()

# Markdown cell
text = """# Task 1: Exploratory Data Analysis & Data Preprocessing
This notebook contains the exploratory data analysis and initial preprocessing for the CFPB complaint dataset.

## Objectives:
1. Load the dataset.
2. Perform EDA (Product distribution, narrative length, missingness).
3. Filter by target products.
4. Clean the complaint narratives.
5. Save the processed dataset."""

nb['cells'] = [nbf.v4.new_markdown_cell(text)]

# Code cell: Imports
code_imports = """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add src to path
sys.path.append(os.path.abspath('../src'))
from preprocessing import clean_narrative, filter_complaints, process_dataset
from eda_utils import perform_eda"""

nb['cells'].append(nbf.v4.new_code_cell(code_imports))

# Code cell: Load Data
code_load = """# Load raw data
raw_data_path = '../data/raw/complaints_sample.csv'
df = pd.read_csv(raw_data_path)
df.head()"""

nb['cells'].append(nbf.v4.new_code_cell(code_load))

# Code cell: EDA
code_eda = """# Perform EDA
df_with_narratives = perform_eda(df)"""

nb['cells'].append(nbf.v4.new_code_cell(code_eda))

# Code cell: Preprocessing
code_prep = """# Filtering and Cleaning
print("Filtering target products and cleaning narratives...")
df_filtered = filter_complaints(df)
df_filtered['cleaned_narrative'] = df_filtered['Consumer complaint narrative'].apply(clean_narrative)

print(f"Filtered dataset size: {len(df_filtered)}")
df_filtered[['Product', 'Consumer complaint narrative', 'cleaned_narrative']].head()"""

nb['cells'].append(nbf.v4.new_code_cell(code_prep))

# Code cell: Save Data
code_save = """# Save processed data
output_path = '../data/processed/filtered_complaints.csv'
if not os.path.exists('../data/processed'):
    os.makedirs('../data/processed')
    
df_filtered.to_csv(output_path, index=False)
print(f"Processed data saved to {output_path}")"""

nb['cells'].append(nbf.v4.new_code_cell(code_save))

# Markdown cell: Summary
summary_text = """## Insights Summary
- **Product Distribution**: ...
- **Narrative Length**: ...
- **Missing Data**: ...
"""
nb['cells'].append(nbf.v4.new_markdown_cell(summary_text))

with open('notebooks/01_eda_preprocessing.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook generated successfully.")
