from __future__ import annotations

import json
import os
import re

import openai

_client_instance: openai.OpenAI | None = None


def _client() -> openai.OpenAI:
    global _client_instance
    if _client_instance is None:
        _client_instance = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client_instance


# The JSON structure GPT needs to fill in — keeping it strict so parsing doesn't break
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
    prompt = ANALYSIS_PROMPT.format(resume=resume_text, job_description=jd_text)
    response = _client().chat.completions.create(
        model="gpt-4o",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.choices[0].message.content.strip()
    # strip markdown fences if the model wraps it anyway
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def extract_keywords(jd_text: str) -> list[str]:
    response = _client().chat.completions.create(
        model="gpt-4o-mini",
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
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def rewrite_summary(current_summary: str, jd_text: str) -> str:
    response = _client().chat.completions.create(
        model="gpt-4o",
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
    return response.choices[0].message.content.strip()
