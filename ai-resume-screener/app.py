import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from analyzer import analyze, extract_keywords, rewrite_summary  # noqa: E402
from parser import parse_resume_file  # noqa: E402
from scorer import get_score_color, score_format  # noqa: E402

st.set_page_config(page_title="AI Resume Screener", page_icon="🤖", layout="wide")
st.title("🤖 AI Resume Screener")
st.caption("Paste or upload your resume + a job description to get an ATS score, skill gaps, and rewrite suggestions")

# ── Input ─────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📄 Your Resume")
    resume_file = st.file_uploader("Upload resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
    resume_text = st.text_area("Or paste resume text here", height=300)
    if resume_file:
        resume_text = parse_resume_file(resume_file)
        st.success(f"Parsed {resume_file.name} — {len(resume_text.split())} words")

with col_right:
    st.subheader("📋 Job Description")
    jd_text = st.text_area("Paste the full job description here", height=300)

analyze_btn = st.button("🚀 Analyze Resume", type="primary", disabled=not (resume_text and jd_text))

# ── Results ───────────────────────────────────────────────────────────────────
if analyze_btn and resume_text and jd_text:
    with st.spinner("Analyzing with AI…"):
        result = analyze(resume_text, jd_text)
        format_check = score_format(resume_text)

    # Score banner
    ats = result.get("ats_score", 0)
    color = get_score_color(ats)
    st.markdown(f"## ATS Score: :{color}[{ats}/100]")

    probability = result.get("interview_probability", "Medium")
    prob_colors = {"Low": "red", "Medium": "orange", "High": "green"}
    p_color = prob_colors.get(probability, "orange")
    st.markdown(f"**Interview Call Probability:** :{p_color}[{probability}]")

    st.divider()

    # ── 4-column summary row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Matched Keywords", len(result.get("matched_keywords", [])))
    c2.metric("Missing Keywords", len(result.get("missing_keywords", [])))
    c3.metric("Format Score", f"{format_check['format_score']}/100")
    c4.metric("Rewrite Suggestions", len(result.get("rewritten_bullets", [])))

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Analysis", "🔑 Keywords", "✍️ Rewrites", "💪 Strengths & Gaps", "🔧 Format Check"]
    )

    with tab1:
        fb = result.get("feedback", {})
        st.markdown("### Overall Assessment")
        st.info(fb.get("overall", ""))
        st.markdown("### Summary Feedback")
        st.write(fb.get("summary", ""))
        st.markdown("### Experience Suggestions")
        for tip in fb.get("experience", []):
            st.markdown(f"- {tip}")
        st.markdown("### Skills Feedback")
        st.write(fb.get("skills", ""))

    with tab2:
        kw_col1, kw_col2 = st.columns(2)
        with kw_col1:
            st.markdown("### ✅ Matched Keywords")
            for kw in result.get("matched_keywords", []):
                st.markdown(f"- `{kw}`")
        with kw_col2:
            st.markdown("### ❌ Missing Keywords")
            for kw in result.get("missing_keywords", []):
                st.markdown(f"- `{kw}`")

        st.divider()
        if st.button("Extract Top JD Keywords"):
            with st.spinner("Extracting…"):
                keywords = extract_keywords(jd_text)
            st.markdown("### Top Keywords from JD")
            st.write(", ".join(f"`{k}`" for k in keywords))

    with tab3:
        bullets = result.get("rewritten_bullets", [])
        if bullets:
            for i, b in enumerate(bullets, 1):
                st.markdown(f"**Bullet {i}**")
                st.error(f"**Original:** {b.get('original', '')}")
                st.success(f"**Improved:** {b.get('improved', '')}")
                st.divider()
        else:
            st.info("No weak bullet points detected.")

        st.markdown("### Rewrite Your Summary")
        current_summary = st.text_area("Paste your current summary:", height=100)
        if st.button("Rewrite Summary") and current_summary:
            with st.spinner("Rewriting…"):
                new_summary = rewrite_summary(current_summary, jd_text)
            st.success(new_summary)

    with tab4:
        s_col, g_col = st.columns(2)
        with s_col:
            st.markdown("### 💪 Top Strengths")
            for s in result.get("top_strengths", []):
                st.markdown(f"- ✅ {s}")
        with g_col:
            st.markdown("### 🚨 Critical Gaps")
            for g in result.get("critical_gaps", []):
                st.markdown(f"- ❗ {g}")

    with tab5:
        st.markdown(f"### Format Score: {format_check['format_score']}/100")
        if format_check["issues"]:
            for issue in format_check["issues"]:
                st.warning(issue)
        else:
            st.success("Your resume format looks great!")
