from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

MAX_INPUT_BYTES = 20 * 1024 * 1024
MAX_INPUT_ROWS = 50_000
MAX_COLUMNS = 64

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
    if not path.is_file():
        raise FileNotFoundError("Input CSV not found or unavailable")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("Connections CSV exceeds the 20 MiB input limit")

    header_row = detect_header_row(path)
    # pandas otherwise silently repairs duplicate column names into ".1" names
    # and may infer numeric/NaN types for private contact fields.
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for _ in range(header_row):
            handle.readline()
        header_line = handle.readline(8193)
    if len(header_line) > 8192:
        raise ValueError("Connections CSV header is too long")
    try:
        columns = [name.strip() for name in next(csv.reader([header_line], strict=True))]
    except (csv.Error, StopIteration) as exc:
        raise ValueError("Invalid Connections CSV header") from exc
    if not columns or len(columns) > MAX_COLUMNS or len(columns) != len(set(columns)):
        raise ValueError("Connections CSV columns are empty, duplicated or excessive")

    dataframe = pd.read_csv(path, skiprows=header_row, encoding="utf-8-sig",
                            dtype=str, keep_default_na=False, nrows=MAX_INPUT_ROWS + 1)
    dataframe.columns = [str(column).strip() for column in dataframe.columns]
    if "Position" not in dataframe.columns:
        raise ValueError("Input CSV must contain a 'Position' column")
    if len(dataframe) == 0 or len(dataframe) > MAX_INPUT_ROWS:
        raise ValueError("Connections CSV is empty or exceeds the 50000-row limit")
    if len(dataframe.columns) != len(columns):
        raise ValueError("Connections CSV has inconsistent columns")
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
