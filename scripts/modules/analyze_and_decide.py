from __future__ import annotations

from pathlib import Path

import pandas as pd

RECOMMENDATIONS = {
    "Product": "Prioritize outreach",
    "AI / Data": "Prioritize outreach",
    "Developer": "Explore collaboration",
    "HR / Recruiter": "Keep warm",
    "Other": "Review manually",
}


def action_recommendation(category: object) -> str:
    """Return a review recommendation; uncertain categories fail to manual review."""
    return RECOMMENDATIONS.get(str(category), "Review manually")


def analyze_and_decide(input_file: str | Path, output_file: str | Path) -> str:
    """Add explainable review recommendations and save them as an Excel workbook."""
    dataframe = pd.read_csv(input_file, encoding="utf-8-sig")
    if "Category" not in dataframe.columns:
        raise ValueError("Categorized input must contain a 'Category' column.")

    dataframe["Action Recommendation"] = dataframe["Category"].apply(action_recommendation)
    dataframe["Recommendation Basis"] = (
        "Role-title heuristic only; review context before taking account actions."
    )

    destination = Path(output_file)
    destination.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_excel(destination, index=False)

    print("Recommendation analysis completed")
    print(
        dataframe.groupby(["Category", "Action Recommendation"], dropna=False)
        .size()
        .to_string()
    )
    return str(destination)
