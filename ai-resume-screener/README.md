# AI Resume Screener

Built this out of frustration. I was applying to jobs and getting no callbacks, but I had no idea if my resume was even making it past ATS filters. Paid tools charge $30/month for this. I figured I could build something better with GPT-4o in a weekend — and I did.

You paste your resume + the job description, and it gives you an ATS compatibility score, tells you exactly which keywords you're missing, and rewrites your weak bullet points with actual impact statements.

---

## Features

- **ATS score (0–100)** — based on keyword match, formatting checks, section completeness
- **Skill gap analysis** — side-by-side matched vs missing keywords from the JD
- **Bullet point rewriter** — takes your vague bullets and makes them quantified and impactful
- **Summary rewriter** — tailors your summary to the specific job
- **FastAPI backend** — in case you want to plug this into something else

## Stack

- Python, Streamlit (frontend)
- FastAPI (REST API backend)
- OpenAI GPT-4o for analysis + rewrites
- pdfplumber + python-docx for parsing resume files

## Getting started

```bash
git clone https://github.com/purnendu1611/ai-resume-screener
cd ai-resume-screener

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # add your OPENAI_API_KEY

# run the UI
streamlit run app.py

# or run the API
uvicorn api:app --reload
```

## How it works

The resume and JD both get sent to GPT-4o with a structured prompt that asks for JSON output — ATS score, matched/missing keywords, specific feedback per section, and rewritten bullets. I then layer a heuristic format checker on top (checks for action verbs, quantified metrics, section presence) because the LLM alone isn't great at catching formatting issues.

## API example

```bash
curl -X POST http://localhost:8000/analyze \
  -F "resume=@my_resume.pdf" \
  -F "job_description=We are looking for a Data Scientist..."
```

## TODO

- [ ] Add support for LinkedIn job URL (auto-scrape the JD)
- [ ] Track score history across multiple applications
- [ ] Better DOCX parsing — tables in Word resumes break things
- [ ] Add a "cover letter generator" tab

## Project layout

```
ai-resume-screener/
├── app.py          # Streamlit UI (5 tabs)
├── api.py          # FastAPI endpoints
├── analyzer.py     # GPT-4o analysis logic
├── parser.py       # PDF/DOCX text extraction
├── scorer.py       # heuristic ATS checks
├── requirements.txt
└── .env.example
```
