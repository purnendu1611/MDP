"""ATS scoring rubric — heuristic checks on top of LLM analysis."""
from __future__ import annotations

import re

SECTION_HEADERS = [
    r"\bsummary\b", r"\bobjective\b", r"\bexperience\b", r"\bwork history\b",
    r"\beducation\b", r"\bskills\b", r"\bprojects\b", r"\bcertifications?\b",
    r"\bachievements?\b",
]

IMPACT_VERBS = [
    "achieved", "built", "designed", "developed", "improved", "increased",
    "launched", "led", "managed", "optimized", "reduced", "saved", "scaled",
    "delivered", "deployed", "automated", "implemented",
]

METRIC_PATTERN = re.compile(r"\b\d+[%xX]?\s*(percent|times|users|clients|hours|days|dollars|\$)?", re.IGNORECASE)


def score_format(resume_text: str) -> dict:
    """Return heuristic format score and issues."""
    issues = []
    score = 100

    text_lower = resume_text.lower()

    # Section presence
    found_sections = sum(1 for p in SECTION_HEADERS if re.search(p, text_lower))
    if found_sections < 4:
        issues.append(f"Only {found_sections}/9 standard sections detected — add missing sections")
        score -= 15

    # Length check
    word_count = len(resume_text.split())
    if word_count < 300:
        issues.append("Resume is too short (under 300 words)")
        score -= 10
    elif word_count > 1200:
        issues.append("Resume may be too long (over 1,200 words)")
        score -= 5

    # Impact verbs
    found_verbs = [v for v in IMPACT_VERBS if v in text_lower]
    if len(found_verbs) < 5:
        issues.append(f"Only {len(found_verbs)} strong action verbs found — aim for 10+")
        score -= 10

    # Quantified metrics
    metrics = METRIC_PATTERN.findall(resume_text)
    if len(metrics) < 3:
        issues.append("Fewer than 3 quantified achievements — add numbers and percentages")
        score -= 10

    # Contact info heuristic
    if "@" not in resume_text:
        issues.append("No email address detected")
        score -= 10

    return {"format_score": max(score, 0), "issues": issues}


def get_score_color(score: int) -> str:
    if score >= 75:
        return "green"
    if score >= 50:
        return "orange"
    return "red"
