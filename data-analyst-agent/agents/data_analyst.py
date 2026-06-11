from __future__ import annotations

import os
import re
import traceback
from io import StringIO

import openai
import pandas as pd

_client_instance: openai.OpenAI | None = None


def _client() -> openai.OpenAI:
    global _client_instance
    if _client_instance is None:
        _client_instance = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client_instance


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

Python code:"""


def _get_schema(df: pd.DataFrame) -> str:
    buf = StringIO()
    df.info(buf=buf)
    return buf.getvalue()


def _extract_code(text: str) -> str:
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def run(df: pd.DataFrame, question: str) -> dict:
    schema = _get_schema(df)
    sample = df.head(3).to_string()

    prompt = CODEGEN_PROMPT.format(schema=schema, sample=sample, question=question)
    response = _client().chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    code = _extract_code(response.choices[0].message.content)

    # exec in a restricted namespace — df is read-only copy so queries can't mutate the original
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
