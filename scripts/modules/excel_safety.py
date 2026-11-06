"""Prevent untrusted contact fields from becoming spreadsheet formulas."""
from __future__ import annotations

import pandas as pd


def _quote_formula(value: object) -> object:
    return ("'" + value) if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")) else value


def safe_for_excel(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Quote formula-looking text in Excel exports; do not alter input CSV."""
    safe = dataframe.copy()
    headers = [_quote_formula(column) for column in safe.columns]
    if len(set(headers)) != len(headers):
        raise ValueError("Spreadsheet-safe headers collide; rename the input columns")
    safe.columns = headers
    for column in safe.columns:
        # pandas 3 defaults to a dedicated string dtype, not object. Inspect
        # cell values rather than skipping those columns.
        safe[column] = safe[column].map(_quote_formula)
    return safe
