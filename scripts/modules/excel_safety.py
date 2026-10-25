"""Prevent untrusted contact fields from becoming spreadsheet formulas."""
from __future__ import annotations

import pandas as pd


def safe_for_excel(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Quote formula-looking text in Excel exports; do not alter input CSV."""
    safe = dataframe.copy()
    for column in safe.columns:
        # pandas 3 defaults to a dedicated string dtype, not object. Inspect
        # cell values rather than skipping those columns.
        safe[column] = safe[column].map(
            lambda value: ("'" + value)
            if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@"))
            else value
        )
    return safe
