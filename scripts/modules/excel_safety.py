"""Prevent untrusted contact fields from becoming spreadsheet formulas."""
from __future__ import annotations

import pandas as pd


def safe_for_excel(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Quote formula-looking text in Excel exports; do not alter input CSV."""
    safe = dataframe.copy()
    for column in safe.columns:
        if safe[column].dtype == object:
            safe[column] = safe[column].map(
                lambda value: ("'" + value)
                if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@"))
                else value
            )
    return safe
