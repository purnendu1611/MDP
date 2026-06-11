"""Narrator Agent — converts data analysis results into plain-English insights."""
from __future__ import annotations

import os

import openai
import pandas as pd

_CLIENT: openai.OpenAI | None = None


def _client() -> openai.OpenAI:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _CLIENT


NARRATE_PROMPT = """\
You are a data storyteller. Turn the following analysis result into a clear, insightful narrative
for a business audience. Be concise (3-5 sentences). Highlight the most important finding first.
Suggest one actionable recommendation based on the data.

User Question: {question}
Analysis Result:
{result}

Narrative:"""


def narrate(question: str, result) -> str:
    """Generate a plain-English explanation of the analysis result."""
    if isinstance(result, pd.DataFrame):
        result_str = result.to_string(max_rows=20)
    elif isinstance(result, pd.Series):
        result_str = result.to_string()
    else:
        result_str = str(result)

    prompt = NARRATE_PROMPT.format(question=question, result=result_str[:2000])
    response = _client().chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()
