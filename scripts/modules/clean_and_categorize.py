import os

import pandas as pd


def clean_and_categorize(input_file, output_dir):
    """
    Read LinkedIn connections CSV, categorize by role,
    and save separate CSVs per category plus a combined CSV.
    """
    df = pd.read_csv(input_file, sep=None, engine='python')

    def categorize(title):
        if pd.isna(title):
            return "Other"
        title = title.lower()
        if any(k in title for k in ["hr", "recruiter", "talent", "people", "human resources"]):
            return "HR / Recruiter"
        elif any(k in title for k in
                 ["developer", "engineer", "cto", "backend", "frontend", "fullstack", "software", "programmer"]):
            return "Developer"
        elif any(k in title for k in ["product", "pm", "product manager", "head of product", "product owner"]):
            return "Product"
        elif any(k in title for k in ["ai", "ml", "data", "machine learning", "deep learning"]):
            return "AI / Data"
        else:
            return "Other"

    df["Category"] = df["Position"].apply(categorize)
    os.makedirs(output_dir, exist_ok=True)

    for cat in df["Category"].unique():
        subset = df[df["Category"] == cat]
        subset.to_csv(os.path.join(output_dir, f"{cat.replace('/', '_')}.csv"), index=False)

    combined_file = os.path.join(output_dir, "all_connections_categorized.csv")
    df.to_csv(combined_file, index=False)
    print("✅ Clean & Categorize Completed")
    print(df["Category"].value_counts())
    return combined_file
