from __future__ import annotations

from pathlib import Path

import pandas as pd

CATEGORY_SCORE = {
    "Product": 5,
    "Developer": 4,
    "AI / Data": 4,
    "HR / Recruiter": 3,
    "Other": 1,
}

COMPLETENESS_FIELDS = ("Company", "Position", "URL")


def _has_value(value: object) -> bool:
    return not pd.isna(value) and bool(str(value).strip())


def compute_priority_score(row: pd.Series) -> int:
    """Compute a deterministic, explainable portfolio-review score."""
    category_points = CATEGORY_SCORE.get(str(row.get("Category", "Other")), 1)
    completeness_points = sum(
        1 for field in COMPLETENESS_FIELDS if field in row and _has_value(row.get(field))
    )
    return int(category_points + completeness_points)


def assign_priority(score: int | float) -> str:
    if score >= 7:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def add_priority_score(input_file: str | Path, output_file: str | Path) -> str:
    """Add deterministic priority fields to a recommendation workbook."""
    dataframe = pd.read_excel(input_file)
    if "Category" not in dataframe.columns:
        raise ValueError("Input workbook must contain a 'Category' column.")

    dataframe["Priority Score"] = dataframe.apply(compute_priority_score, axis=1)
    dataframe["Priority"] = dataframe["Priority Score"].apply(assign_priority)
    dataframe["Priority Basis"] = (
        "Category relevance (1-5) + presence of Company/Position/URL (0-3)."
    )

    destination = Path(output_file)
    destination.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_excel(destination, index=False)

    print("Priority scoring completed")
    print(dataframe.groupby("Priority").size().to_string())
    return str(destination)


def add_engagement_score(input_file: str | Path, output_file: str | Path) -> str:
    """Backward-compatible alias for the former random engagement-score function."""
    return add_priority_score(input_file, output_file)
