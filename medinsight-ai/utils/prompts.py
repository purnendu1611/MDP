from langchain.prompts import PromptTemplate

MEDICAL_QA_TEMPLATE = """You are a knowledgeable medical assistant helping patients understand their medical reports.
Use ONLY the provided context to answer the question. If the information is not in the context, say so clearly.
Always note that your answers are informational and not a substitute for professional medical advice.

Context from medical reports:
{context}

Patient Question: {question}

Answer (be specific, mention units and reference ranges where applicable):"""

MEDICAL_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=MEDICAL_QA_TEMPLATE,
)

SUMMARY_TEMPLATE = """You are a medical assistant. Summarize the following medical report content in plain English
for a patient with no medical background. Structure your summary as:

1. **Key Findings** — main results in simple terms
2. **Values to Watch** — any abnormal or borderline values
3. **Recommended Actions** — any follow-ups or lifestyle changes mentioned
4. **Overall Assessment** — 1-2 sentence plain-English conclusion

Medical Report:
{report_text}

Summary:"""

SUMMARY_PROMPT = SUMMARY_TEMPLATE
