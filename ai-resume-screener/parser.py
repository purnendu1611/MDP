from __future__ import annotations

import io
from pathlib import Path

import pdfplumber
from docx import Document


def parse_pdf(file_obj) -> str:
    """Extract text from an uploaded PDF file object."""
    pages: list[str] = []
    with pdfplumber.open(io.BytesIO(file_obj.read())) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
    return "\n\n".join(pages)


def parse_docx(file_obj) -> str:
    """Extract text from an uploaded DOCX file object."""
    doc = Document(io.BytesIO(file_obj.read()))
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


def parse_resume_file(file_obj) -> str:
    """Auto-detect file type and extract text."""
    name = file_obj.name.lower()
    if name.endswith(".pdf"):
        return parse_pdf(file_obj)
    if name.endswith(".docx"):
        return parse_docx(file_obj)
    # Plain text
    return file_obj.read().decode("utf-8", errors="ignore")
