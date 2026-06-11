"""Orchestrator — routes user queries to the right agent(s) and assembles results."""
from __future__ import annotations

import pandas as pd

from agents.chart_generator import build as build_chart
from agents.data_analyst import run as run_analysis
from agents.narrator import narrate
from agents.statistics_agent import full_eda


def run_query(df: pd.DataFrame, question: str) -> dict:
    """
    Route the question through the multi-agent pipeline:
      1. DataAnalyst  → code + raw result
      2. ChartGenerator → Plotly figure (optional)
      3. Narrator → plain-English insight
    """
    # Step 1: Generate and execute analysis code
    analysis = run_analysis(df, question)

    if not analysis["success"]:
        return {
            "success": False,
            "question": question,
            "error": analysis["error"],
            "code": analysis["code"],
            "result": None,
            "figure": None,
            "narrative": None,
        }

    result = analysis["result"]

    # Step 2: Build chart
    figure = None
    try:
        figure = build_chart(question, result, df)
    except Exception:
        figure = None

    # Step 3: Narrate
    narrative = narrate(question, result)

    return {
        "success": True,
        "question": question,
        "code": analysis["code"],
        "result": result,
        "figure": figure,
        "narrative": narrative,
        "error": None,
    }


def run_eda(df: pd.DataFrame) -> dict:
    """Run automated Exploratory Data Analysis."""
    return full_eda(df)
