# MedInsight AI

I built this after my dad got a bunch of lab reports post-surgery and neither of us could make sense of them. We kept googling every term separately. So I figured — why not just build something that lets you upload the PDF and ask questions directly?

It uses RAG (Retrieval Augmented Generation) — basically it chunks up the report, stores it in a vector DB, and when you ask a question it retrieves the relevant parts and sends them to GPT-4o for an answer. Nothing too fancy but it actually works pretty well on real reports.

---

## What it does

- Upload one or more medical PDFs (blood tests, discharge summaries, radiology reports, etc.)
- Ask plain-English questions: *"Is my hemoglobin normal?"*, *"What medications were prescribed?"*
- Get answers with the exact source highlighted so you can verify
- Generate a plain-English summary of the whole report
- Flags values that look abnormal based on standard reference ranges

## Tech used

- Python, Streamlit for the UI
- LangChain for the RAG pipeline
- ChromaDB as the vector store
- OpenAI GPT-4o for answering + embeddings
- pdfplumber / PyPDF2 for parsing

## Setup

```bash
git clone https://github.com/purnendu1611/medinsight-ai
cd medinsight-ai

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# open .env and paste your OpenAI API key

streamlit run app.py
```

Then go to `http://localhost:8501`, upload a PDF, and start asking questions.

## Project structure

```
medinsight-ai/
├── app.py              # Streamlit UI
├── rag_pipeline.py     # core RAG logic (chunking, embedding, retrieval)
├── utils/
│   ├── pdf_processor.py
│   ├── risk_analyzer.py   # reference ranges for common lab values
│   └── prompts.py
├── requirements.txt
└── .env.example
```

## Known issues / TODO

- [ ] Handwritten or scanned PDFs don't parse well — need OCR integration
- [ ] Reference ranges are hardcoded, should be age/gender aware
- [ ] Would be nice to add a "compare reports over time" feature
- [ ] Haven't tested on radiology reports much, mostly works on blood panels

## What I learned

Chunking strategy matters a lot more than I expected. My first version used fixed 500-char chunks and the answers were terrible because lab values would get split across chunks. Switching to sentence-aware splitting with overlap fixed most of it.

---

> **Disclaimer:** This is a personal project for learning. Not a substitute for professional medical advice.
