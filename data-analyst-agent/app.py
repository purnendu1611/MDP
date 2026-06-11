import json

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from orchestrator import run_eda, run_query  # noqa: E402
from utils.data_loader import load_file  # noqa: E402

st.set_page_config(page_title="Data Analyst Agent", page_icon="📊", layout="wide")
st.title("📊 Data Analyst Agent")
st.caption("Upload any CSV/Excel → ask questions in plain English → get instant charts & insights")

# ── Upload ────────────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx", "xls"])

if uploaded:
    df: pd.DataFrame = load_file(uploaded)
    st.session_state["df"] = df
    st.success(f"Loaded **{uploaded.name}** — {df.shape[0]:,} rows × {df.shape[1]} columns")

    with st.expander("👀 Preview Data"):
        st.dataframe(df.head(20), use_container_width=True)

df: pd.DataFrame | None = st.session_state.get("df")

if df is None:
    st.info("Upload a CSV or Excel file to get started.")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_query, tab_eda, tab_history = st.tabs(["💬 Ask Questions", "📈 Auto EDA", "🕒 History"])

# ── Query Tab ─────────────────────────────────────────────────────────────────
with tab_query:
    st.subheader("Ask anything about your data")

    col_q, col_ex = st.columns([3, 1])
    with col_q:
        question = st.text_input(
            "Your question",
            placeholder="e.g. Which age group has the highest diabetes risk?",
        )
    with col_ex:
        st.markdown("**Quick examples:**")
        examples = [
            "Show total count by each category",
            "What are the top 5 rows by value?",
            "Find correlation between numeric columns",
            "Detect outliers in the main numeric column",
            "Show distribution of the first numeric column",
        ]
        for ex in examples:
            if st.button(ex, key=ex):
                question = ex

    if st.button("🔍 Analyze", type="primary") and question:
        with st.spinner("Multi-agent analysis in progress…"):
            output = run_query(df, question)

        if output["success"]:
            # Narrative
            st.markdown("### 💡 Insight")
            st.info(output["narrative"])

            # Chart
            if output["figure"]:
                st.markdown("### 📊 Visualization")
                st.plotly_chart(output["figure"], use_container_width=True)

            # Raw result
            result = output["result"]
            st.markdown("### 📋 Data Result")
            if isinstance(result, pd.DataFrame):
                st.dataframe(result, use_container_width=True)
            elif isinstance(result, pd.Series):
                st.dataframe(result.reset_index(), use_container_width=True)
            else:
                st.write(result)

            # Code transparency
            with st.expander("🔎 View Generated Code"):
                st.code(output["code"], language="python")

            # Save to history
            if "history" not in st.session_state:
                st.session_state["history"] = []
            st.session_state["history"].append(
                {"question": question, "narrative": output["narrative"]}
            )
        else:
            st.error("Analysis failed.")
            with st.expander("Error details"):
                st.code(output["error"])
            st.info("Try rephrasing your question.")

# ── EDA Tab ───────────────────────────────────────────────────────────────────
with tab_eda:
    st.subheader("Automated Exploratory Data Analysis")
    if st.button("🚀 Run Full EDA", type="primary"):
        with st.spinner("Running EDA…"):
            eda = run_eda(df)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{eda['shape']['rows']:,}")
        c2.metric("Columns", eda['shape']['columns'])
        c3.metric("Columns with Missing Data", len(eda['missing_values']))
        c4.metric("Duplicate Rows", eda['duplicate_rows'])

        if eda["missing_values"]:
            st.markdown("### ⚠️ Missing Values")
            mv_df = pd.DataFrame(eda["missing_values"]).T
            st.dataframe(mv_df, use_container_width=True)

        if eda["numeric_summary"]:
            st.markdown("### 📐 Numeric Summary")
            st.dataframe(pd.DataFrame(eda["numeric_summary"]).T, use_container_width=True)

        if eda.get("top_correlations"):
            st.markdown("### 🔗 Top Correlations")
            for pair, val in eda["top_correlations"].items():
                color = "green" if abs(val) > 0.7 else ("orange" if abs(val) > 0.4 else "gray")
                st.markdown(f"- **{pair}**: :{color}[{val}]")

        if eda["categorical_summary"]:
            st.markdown("### 🏷️ Categorical Columns")
            for col, info in eda["categorical_summary"].items():
                with st.expander(f"{col} — {info['unique_values']} unique values"):
                    st.bar_chart(pd.Series(info["top_5"]))

# ── History Tab ───────────────────────────────────────────────────────────────
with tab_history:
    history = st.session_state.get("history", [])
    if not history:
        st.info("No queries yet in this session.")
    else:
        for i, item in enumerate(reversed(history), 1):
            st.markdown(f"**Q{i}: {item['question']}**")
            st.caption(item["narrative"])
            st.divider()
