"""Narrator Agent — converts data analysis results into plain-English insights."""
from __future__ import annotations

import os

import anthropic
import pandas as pd

_CLIENT: anthropic.Anthropic | None = None


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
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
    message = _client().messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()
