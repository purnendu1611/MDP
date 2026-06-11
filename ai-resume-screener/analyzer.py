from __future__ import annotations

import json
import os
import re

import anthropic

_CLIENT: anthropic.Anthropic | None = None


def _client() -> anthropic.Anthropic:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _CLIENT


ANALYSIS_PROMPT = """\
You are an expert ATS (Applicant Tracking System) and HR consultant.

Analyze the provided resume against the job description and return a JSON object with this exact structure:
{{
  "ats_score": <integer 0-100>,
  "matched_keywords": [<list of keywords from JD found in resume>],
  "missing_keywords": [<list of important JD keywords missing from resume>],
  "feedback": {{
    "summary": "<feedback on the professional summary>",
    "experience": [<list of specific improvement suggestions>],
    "skills": "<feedback on skills section>",
    "overall": "<2-3 sentence holistic assessment>"
  }},
  "rewritten_bullets": [
    {{
      "original": "<weak bullet from resume>",
      "improved": "<stronger, quantified version>"
    }}
  ],
  "interview_probability": "<Low | Medium | High>",
  "top_strengths": [<list of 3 resume strengths>],
  "critical_gaps": [<list of top 3 missing qualifications>]
}}

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON. No explanation or markdown."""


def analyze(resume_text: str, jd_text: str) -> dict:
    """Call Claude to analyze the resume against the JD and return structured results."""
    prompt = ANALYSIS_PROMPT.format(resume=resume_text, job_description=jd_text)
    message = _client().messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def extract_keywords(jd_text: str) -> list[str]:
    """Extract top technical and soft-skill keywords from a job description."""
    message = _client().messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the 15 most important keywords (skills, technologies, qualifications) "
                    f"from this job description. Return as a JSON array of strings only.\n\n{jd_text}"
                ),
            }
        ],
    )
    raw = message.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def rewrite_summary(current_summary: str, jd_text: str) -> str:
    """Rewrite the resume summary to better match the JD."""
    message = _client().messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    "Rewrite this resume professional summary to better match the job description. "
                    "Keep it under 4 sentences. Be specific, impactful, and use keywords from the JD.\n\n"
                    f"Current Summary:\n{current_summary}\n\nJob Description:\n{jd_text}\n\nRewritten Summary:"
                ),
            }
        ],
    )
    return message.content[0].text.strip()
