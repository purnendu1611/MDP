# 🤖 AI Resume Screener — Intelligent Resume Analyzer & JD Matcher

> Paste your resume and a job description — get an ATS compatibility score, skill gap analysis, and personalized rewrite suggestions powered by LLMs.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110-orange)

---

## Features

- **ATS Score (0–100)** — keyword match, format check, section completeness
- **Skill Gap Analysis** — missing skills vs. job description requirements
- **Section-by-Section Feedback** — summary, experience, education, skills
- **Rewrite Suggestions** — AI rewrites weak bullet points to be more impactful
- **Keyword Optimizer** — extracts must-have keywords from any JD
- **Multi-JD Comparison** — check your resume against multiple job postings at once
- **PDF/DOCX support** — upload resume files directly

## Architecture

```
  Resume (PDF/DOCX/Text)          Job Description (Text/URL)
         │                                   │
         ▼                                   ▼
   Resume Parser                       JD Extractor
  (sections, skills,              (requirements, skills,
   experience, keywords)           qualifications, keywords)
         │                                   │
         └──────────────┬────────────────────┘
                        ▼
              LLM Analysis Engine (GPT-4o)
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
     ATS Score    Skill Gaps    Rewrite Suggestions
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | OpenAI GPT-4o |
| Backend | FastAPI |
| UI | Streamlit |
| PDF Parsing | pdfplumber, python-docx |
| NLP | spaCy, sentence-transformers |
| Scoring | Custom rubric + LLM judge |

## Setup

```bash
git clone https://github.com/purnendu1611/ai-resume-screener
cd ai-resume-screener
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY to .env
streamlit run app.py
```

## API Usage (FastAPI backend)

```bash
uvicorn api:app --reload

# Analyze a resume
curl -X POST http://localhost:8000/analyze \
  -F "resume=@my_resume.pdf" \
  -F "job_description=We are looking for a Data Scientist with 3+ years..."
```

**Response:**
```json
{
  "ats_score": 78,
  "matched_keywords": ["Python", "Machine Learning", "SQL"],
  "missing_keywords": ["dbt", "Airflow", "LLMs"],
  "feedback": {
    "summary": "Strong background but lacks mention of cloud platforms.",
    "experience": ["Quantify achievements with metrics", "Add impact statements"],
    "skills": "Add LLM/GenAI skills to match modern JD requirements"
  },
  "rewritten_bullets": [
    {
      "original": "Worked on ML models",
      "improved": "Developed and deployed 5 ML classification models achieving 94% accuracy, reducing manual review time by 40%"
    }
  ]
}
```

## Project Structure

```
ai-resume-screener/
├── app.py                  # Streamlit UI
├── api.py                  # FastAPI endpoints
├── analyzer.py             # Core analysis logic
├── parser.py               # Resume & JD parsing
├── scorer.py               # ATS scoring rubric
├── prompts.py              # LLM prompt templates
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT
