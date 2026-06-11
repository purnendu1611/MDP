import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from rag_pipeline import MedicalRAGPipeline  # noqa: E402

st.set_page_config(page_title="MedInsight AI", page_icon="🏥", layout="wide")

st.title("🏥 MedInsight AI")
st.caption("Intelligent Medical Report Analysis powered by RAG + LLMs")


@st.cache_resource
def get_pipeline() -> MedicalRAGPipeline:
    return MedicalRAGPipeline()


pipeline = get_pipeline()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📂 Upload Medical Reports")
    uploaded_files = st.file_uploader(
        "PDF reports (blood tests, radiology, discharge summaries)",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        if st.button("⚙️ Process Documents", type="primary"):
            total_chunks = 0
            with st.spinner("Extracting text and building knowledge base…"):
                for f in uploaded_files:
                    total_chunks += pipeline.add_document(f)
            st.success(f"Indexed {len(uploaded_files)} file(s) — {total_chunks} chunks stored.")

    st.divider()
    if st.button("🗑️ Clear All Documents"):
        pipeline.clear()
        st.info("Knowledge base cleared.")

# ── Main Layout ───────────────────────────────────────────────────────────────
col_chat, col_summary = st.columns([3, 2])

with col_chat:
    st.subheader("💬 Ask Questions")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("e.g. Is my hemoglobin level normal?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing reports…"):
                result = pipeline.query(prompt)

            st.markdown(result["answer"])

            if result["sources"]:
                with st.expander("📄 Source References"):
                    for i, src in enumerate(result["sources"], 1):
                        st.markdown(
                            f"**[{i}] {src['file']} — Page {src['page']}**\n\n"
                            f"> {src['content'][:300]}…"
                        )

        st.session_state.messages.append(
            {"role": "assistant", "content": result["answer"]}
        )

with col_summary:
    st.subheader("📋 Report Summary")
    if st.button("Generate Plain-English Summary"):
        with st.spinner("Summarizing…"):
            summary = pipeline.summarize()
        st.markdown(summary)

    st.divider()
    st.subheader("💡 Suggested Questions")
    suggestions = [
        "What are the key abnormal values?",
        "What medications were prescribed?",
        "What follow-up tests were recommended?",
        "Is there any indication of diabetes or cardiovascular risk?",
        "Summarize the patient's current health status.",
    ]
    for q in suggestions:
        if st.button(q, key=q):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()
