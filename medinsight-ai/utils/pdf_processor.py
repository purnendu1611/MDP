from __future__ import annotations

import re
from pathlib import Path

import pdfplumber


def extract_text_from_pdf(path: str | Path) -> str:
    """Extract cleaned text from a PDF file."""
    pages: list[str] = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
    return "\n\n".join(pages)


def extract_tables_from_pdf(path: str | Path) -> list[dict]:
    """Extract tabular data (e.g., lab results) from PDF pages."""
    tables = []
    with pdfplumber.open(str(path)) as pdf:
        for i, page in enumerate(pdf.pages):
            for table in page.extract_tables():
                if table:
                    tables.append({"page": i + 1, "data": table})
    return tables


_ABNORMAL_PATTERNS = [
    r"\bHIGH\b", r"\bLOW\b", r"\bABNORMAL\b", r"\bCRITICAL\b",
    r"\bOUT OF RANGE\b", r"\bPOSITIVE\b(?! control)",
    r"[↑↓]",
]
_COMPILED = [re.compile(p, re.IGNORECASE) for p in _ABNORMAL_PATTERNS]


def flag_abnormal_values(text: str) -> list[str]:
    """Return lines from the text that contain potential abnormal markers."""
    flagged = []
    for line in text.splitlines():
        if any(pat.search(line) for pat in _COMPILED):
            flagged.append(line.strip())
    return flagged
