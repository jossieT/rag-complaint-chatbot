import pandas as pd
import numpy as np

# CFPB Columns
columns = [
    "Date received", "Product", "Sub-product", "Issue", "Sub-issue",
    "Consumer complaint narrative", "Company public response", "Company",
    "State", "ZIP code", "Tags", "Consumer consent provided?", "Submitted via",
    "Date sent to company", "Company response to consumer", "Timely response?",
    "Consumer disputed?", "Complaint ID"
]

# Sample data
products = [
    "Credit card or prepaid card", 
    "Payday loan, title loan, or personal loan",
    "Checking or savings account", 
    "Money transfer, virtual currency, or money service",
    "Mortgage",
    "Student loan"
]

narratives = [
    "I am writing to file a complaint about my credit card. There are charges I didn't make.",
    "My personal loan has a very high interest rate that wasn't disclosed.",
    "I cannot access my savings account. The bank is not helping.",
    "The money transfer never arrived at the destination.",
    "I'm having trouble with my mortgage payments.",
    "I have a problem with my credit card billing. I am writing to file a complaint."
]

data = []
for i in range(100):
    idx = i % len(products)
    row = [
        "2023-01-01", 
        products[idx], 
        "Sub-product " + str(idx), 
        "Issue " + str(idx), 
        "Sub-issue " + str(idx),
        narratives[idx] if i % 5 != 0 else np.nan, # some missing narratives
        "Company response", 
        "Company XYZ", 
        "NY", 
        "10001", 
        "None", 
        "Consent provided", 
        "Web", 
        "2023-01-02", 
        "Closed with explanation", 
        "Yes", 
        "No", 
        1000000 + i
    ]
    data.append(row)

df = pd.DataFrame(data, columns=columns)
df.to_csv("data/raw/complaints_sample.csv", index=False)
print("Synthetic sample generated: data/raw/complaints_sample.csv")
