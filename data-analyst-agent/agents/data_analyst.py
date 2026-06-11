"""Data Analyst Agent — generates and executes Pandas code to answer queries."""
from __future__ import annotations

import os
import re
import traceback
from io import StringIO

import anthropic
import pandas as pd

_CLIENT: anthropic.Anthropic | None = None


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _CLIENT


CODEGEN_PROMPT = """\
You are a senior data analyst. Given the DataFrame schema and a user question, write Python/Pandas code to answer it.

DataFrame name: `df`
Schema:
{schema}

Sample rows:
{sample}

User question: {question}

Rules:
- Write ONLY executable Python code, no explanations
- Store the final answer in a variable called `result`
- `result` can be a DataFrame, Series, scalar, or dict
- Do NOT import pandas — it is already imported as `pd`
- Do NOT read any files — `df` is already loaded
- Handle edge cases (empty results, missing columns)

Python code:"""


def _get_schema(df: pd.DataFrame) -> str:
    buf = StringIO()
    df.info(buf=buf)
    return buf.getvalue()


def _extract_code(text: str) -> str:
    """Extract code block from LLM response."""
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def run(df: pd.DataFrame, question: str) -> dict:
    """Generate code for the question, execute it, and return result + code."""
    schema = _get_schema(df)
    sample = df.head(3).to_string()

    prompt = CODEGEN_PROMPT.format(schema=schema, sample=sample, question=question)
    message = _client().messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    code = _extract_code(message.content[0].text)

    # Execute code in sandboxed namespace
    namespace = {"df": df.copy(), "pd": pd}
    try:
        exec(code, namespace)  # noqa: S102
        result = namespace.get("result", "No result variable set.")
    except Exception:
        return {
            "success": False,
            "code": code,
            "error": traceback.format_exc(),
            "result": None,
        }

    return {"success": True, "code": code, "result": result, "error": None}
