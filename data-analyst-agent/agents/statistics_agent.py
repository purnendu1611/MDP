"""Statistics Agent — automated EDA and statistical summaries."""
from __future__ import annotations

import pandas as pd


def full_eda(df: pd.DataFrame) -> dict:
    """Return a comprehensive EDA summary for the given DataFrame."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    summary = {
        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "column_types": df.dtypes.astype(str).to_dict(),
        "missing_values": {
            col: {"count": int(missing[col]), "percent": float(missing_pct[col])}
            for col in df.columns
            if missing[col] > 0
        },
        "numeric_summary": df[numeric_cols].describe().round(3).to_dict() if numeric_cols else {},
        "categorical_summary": {
            col: {
                "unique_values": int(df[col].nunique()),
                "top_5": df[col].value_counts().head(5).to_dict(),
            }
            for col in categorical_cols
        },
        "duplicate_rows": int(df.duplicated().sum()),
    }

    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        # Find top 5 highest absolute correlations (excluding self-correlations)
        corr_pairs = (
            corr.where(~(corr == 1.0))
            .stack()
            .abs()
            .sort_values(ascending=False)
            .head(5)
        )
        summary["top_correlations"] = {
            f"{a} ↔ {b}": round(float(corr.loc[a, b]), 3)
            for (a, b) in corr_pairs.index
        }

    return summary


def detect_outliers(df: pd.DataFrame, column: str) -> dict:
    """IQR-based outlier detection for a numeric column."""
    if column not in df.columns:
        return {"error": f"Column '{column}' not found"}

    series = df[column].dropna()
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = series[(series < lower) | (series > upper)]

    return {
        "column": column,
        "total_values": len(series),
        "outlier_count": len(outliers),
        "outlier_percent": round(len(outliers) / len(series) * 100, 2),
        "lower_bound": round(lower, 3),
        "upper_bound": round(upper, 3),
        "outlier_values": outliers.tolist()[:10],
    }
