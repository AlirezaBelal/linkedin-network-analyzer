from __future__ import annotations

from pathlib import Path

import pandas as pd

CATEGORY_FILENAMES = {
    "HR / Recruiter": "HR _ Recruiter.csv",
    "Developer": "Developer.csv",
    "Product": "Product.csv",
    "AI / Data": "AI _ Data.csv",
    "Other": "Other.csv",
}


def categorize_title(title: object) -> str:
    """Categorize a role title using transparent keyword heuristics."""
    if pd.isna(title):
        return "Other"

    normalized = str(title).strip().lower()
    if not normalized:
        return "Other"

    if any(
        keyword in normalized
        for keyword in ("hr", "recruiter", "talent", "people", "human resources")
    ):
        return "HR / Recruiter"

    if any(
        keyword in normalized
        for keyword in (
            "machine learning",
            "deep learning",
            "data scientist",
            "data analyst",
            "data engineer",
            "ai engineer",
            "ml engineer",
            "artificial intelligence",
        )
    ) or normalized.startswith(("ai ", "ml ", "data ")):
        return "AI / Data"

    if any(
        keyword in normalized
        for keyword in (
            "product manager",
            "head of product",
            "product owner",
            "product lead",
            "product",
        )
    ) or normalized == "pm":
        return "Product"

    if any(
        keyword in normalized
        for keyword in (
            "developer",
            "engineer",
            "cto",
            "backend",
            "frontend",
            "fullstack",
            "full stack",
            "software",
            "programmer",
        )
    ):
        return "Developer"

    return "Other"


def detect_header_row(input_file: str | Path, max_lines: int = 12) -> int:
    """Find a LinkedIn-style CSV header even when explanatory lines precede it."""
    path = Path(input_file)
    with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        for index, line in enumerate(handle):
            if index >= max_lines:
                break
            lowered = line.lower()
            if "position" in lowered and ("first name" in lowered or "last name" in lowered):
                return index
    return 0


def read_connections_csv(input_file: str | Path) -> pd.DataFrame:
    path = Path(input_file)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    header_row = detect_header_row(path)
    dataframe = pd.read_csv(path, skiprows=header_row, encoding="utf-8-sig")
    dataframe.columns = [str(column).strip() for column in dataframe.columns]

    if "Position" not in dataframe.columns:
        raise ValueError(
            "Input CSV must contain a 'Position' column. "
            "Use a LinkedIn connections export or a compatible CSV."
        )

    return dataframe


def clean_and_categorize(input_file: str | Path, output_dir: str | Path) -> str:
    """Read a connections CSV, categorize titles, and write reviewable CSV outputs."""
    dataframe = read_connections_csv(input_file)
    dataframe["Category"] = dataframe["Position"].apply(categorize_title)

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    for category, filename in CATEGORY_FILENAMES.items():
        subset = dataframe[dataframe["Category"] == category]
        if not subset.empty:
            subset.to_csv(destination / filename, index=False, encoding="utf-8-sig")

    combined_file = destination / "all_connections_categorized.csv"
    dataframe.to_csv(combined_file, index=False, encoding="utf-8-sig")

    print("Clean & categorize completed")
    print(dataframe["Category"].value_counts().to_string())
    return str(combined_file)
