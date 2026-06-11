"""Chart Generator Agent — decides chart type and builds Plotly figures."""
from __future__ import annotations

import json
import os
import re

import openai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

_CLIENT: openai.OpenAI | None = None


def _client() -> openai.OpenAI:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _CLIENT


CHART_PLAN_PROMPT = """\
Given the user question and the DataFrame result, decide the best chart type and configuration.

User question: {question}
Result type: {result_type}
Result preview: {preview}
DataFrame columns: {columns}

Return a JSON object with:
{{
  "chart_type": "bar|line|scatter|histogram|box|heatmap|pie|none",
  "x": "<column name or null>",
  "y": "<column name or null>",
  "color": "<column name or null>",
  "title": "<chart title>",
  "reason": "<why this chart type>"
}}

Return ONLY valid JSON."""


def _plan_chart(question: str, result, df_columns: list[str]) -> dict:
    result_type = type(result).__name__
    if isinstance(result, (pd.DataFrame, pd.Series)):
        preview = result.head(5).to_string()
    else:
        preview = str(result)[:300]

    prompt = CHART_PLAN_PROMPT.format(
        question=question,
        result_type=result_type,
        preview=preview,
        columns=", ".join(df_columns),
    )
    response = _client().chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def build(question: str, result, original_df: pd.DataFrame):
    """Return a Plotly figure or None if a chart isn't appropriate."""
    if result is None:
        return None

    plan = _plan_chart(question, result, list(original_df.columns))

    if plan.get("chart_type") == "none":
        return None

    data = result if isinstance(result, pd.DataFrame) else original_df
    chart_type = plan.get("chart_type", "bar")
    x = plan.get("x")
    y = plan.get("y")
    color = plan.get("color")
    title = plan.get("title", question[:60])

    try:
        if chart_type == "bar":
            fig = px.bar(data, x=x, y=y, color=color, title=title)
        elif chart_type == "line":
            fig = px.line(data, x=x, y=y, color=color, title=title)
        elif chart_type == "scatter":
            fig = px.scatter(data, x=x, y=y, color=color, title=title)
        elif chart_type == "histogram":
            fig = px.histogram(data, x=x, color=color, title=title)
        elif chart_type == "box":
            fig = px.box(data, x=x, y=y, color=color, title=title)
        elif chart_type == "pie":
            fig = px.pie(data, names=x, values=y, title=title)
        elif chart_type == "heatmap":
            numeric = data.select_dtypes(include="number")
            fig = px.imshow(numeric.corr(), title=title, text_auto=True)
        else:
            fig = px.bar(data, x=x, y=y, title=title)

        fig.update_layout(template="plotly_white")
        return fig
    except Exception:
        return None
