import os

import pandas as pd


def analyze_and_decide(input_file, output_file):
    """
    Add action recommendation for each connection based on category
    and save as Excel.
    """
    df = pd.read_csv(input_file)

    def action_recommendation(category):
        if category == "Product":
            return "Engage / Follow"
        elif category == "Developer":
            return "Collaborate / Follow"
        elif category == "HR / Recruiter":
            return "Keep / Follow"
        elif category == "AI / Data":
            return "Engage / Follow"
        else:
            return "Unfollow / Remove"

    df["Action Recommendation"] = df["Category"].apply(action_recommendation)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_excel(output_file, index=False)

    print("✅ Analyze & Decide Completed")
    print(df.groupby(["Category", "Action Recommendation"]).size())
    return output_file
