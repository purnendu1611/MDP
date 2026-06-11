from __future__ import annotations

import io

import pandas as pd


def load_file(file_obj) -> pd.DataFrame:
    """Load a CSV or Excel file object into a DataFrame."""
    name = file_obj.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file_obj)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_obj)
    raise ValueError(f"Unsupported file type: {file_obj.name}")


def get_info(df: pd.DataFrame) -> str:
    """Return a human-readable summary of the DataFrame."""
    buf = io.StringIO()
    df.info(buf=buf)
    return buf.getvalue()
