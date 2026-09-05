import os

import pandas as pd


def add_engagement_score(input_file, output_file):
    """
    Add Engagement Score and Priority based on Category and dummy Activity.
    """
    df = pd.read_excel(input_file)

    # Assign score based on category (weight)
    category_score = {
        "Product": 5,
        "Developer": 4,
        "AI / Data": 4,
        "HR / Recruiter": 3,
        "Other": 1
    }

    # Dummy recent activity score (simulate: 1-3)
    import random
    df["Activity Score"] = df["Category"].apply(lambda x: random.randint(1, 3))

    # Engagement Score = Category Score + Activity Score
    df["Engagement Score"] = df["Category"].map(category_score) + df["Activity Score"]

    # Priority assignment
    def assign_priority(score):
        if score >= 8:
            return "High"
        elif score >= 6:
            return "Medium"
        else:
            return "Low"

    df["Priority"] = df["Engagement Score"].apply(assign_priority)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_excel(output_file, index=False)

    print("✅ Engagement Score & Priority Added")
    print(df.groupby("Priority").size())
    return output_file
