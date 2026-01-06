import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def perform_eda(df, output_dir='docs/images'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print("--- Dataset Overview ---")
    print(f"Total complaints: {len(df)}")
    print("\nMissing narratives:")
    missing_narratives = df['Consumer complaint narrative'].isna().sum()
    perc_missing = (missing_narratives / len(df)) * 100
    print(f"{missing_narratives} ({perc_missing:.2f}%)")
    
    # Distribution of complaints by product
    plt.figure(figsize=(12, 6))
    sns.countplot(y='Product', data=df, order=df['Product'].value_counts().index)
    plt.title('Distribution of Complaints by Product')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/product_distribution.png')
    # plt.show()
    
    # Narrative length distribution
    df_with_narrative = df[df['Consumer complaint narrative'].notna()].copy()
    df_with_narrative['narrative_word_count'] = df_with_narrative['Consumer complaint narrative'].str.split().str.len()
    
    plt.figure(figsize=(10, 6))
    sns.histplot(df_with_narrative['narrative_word_count'], bins=50, kde=True)
    plt.title('Distribution of Complaint Narrative Word Count')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.savefig(f'{output_dir}/narrative_length_dist.png')
    # plt.show()
    
    print("\nNarrative length statistics:")
    print(df_with_narrative['narrative_word_count'].describe())
    
    return df_with_narrative
