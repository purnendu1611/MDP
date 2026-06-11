"""FastAPI backend — REST API wrapper around the analyzer."""
from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from analyzer import analyze, extract_keywords
from parser import parse_resume_file
from scorer import score_format

app = FastAPI(title="AI Resume Screener API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Analyze a resume file against a job description."""
    try:
        resume_text = parse_resume_file(resume)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse resume: {e}") from e

    try:
        result = analyze(resume_text, job_description)
        result["format_check"] = score_format(resume_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/keywords")
async def get_keywords(job_description: str = Form(...)):
    """Extract top keywords from a job description."""
    return {"keywords": extract_keywords(job_description)}


@app.post("/analyze-text")
async def analyze_text(resume_text: str = Form(...), job_description: str = Form(...)):
    """Analyze plain-text resume against a job description."""
    result = analyze(resume_text, job_description)
    result["format_check"] = score_format(resume_text)
    return result
