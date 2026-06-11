# 🏥 MedInsight AI — Medical Report Analyzer & Chatbot

> RAG-powered chatbot that lets you upload medical reports (PDF/text) and ask questions in plain English. Built with LangChain, ChromaDB, and Claude/OpenAI.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![LangChain](https://img.shields.io/badge/LangChain-0.2-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red) ![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5-purple)

---

## Features

- **Upload** PDF medical reports (blood tests, radiology, discharge summaries)
- **Ask** natural language questions: *"Is my hemoglobin normal?"*, *"What medications were prescribed?"*
- **Summarize** entire reports in plain English
- **Multi-document** support — query across multiple reports simultaneously
- **Source citations** — see exactly which part of the report the answer came from
- **Risk Flagging** — highlights abnormal values and suggests follow-up questions

## Architecture

```
User uploads PDF
      │
      ▼
 PDF Loader (PyPDF2)
      │
      ▼
 Text Chunking (RecursiveCharacterTextSplitter)
      │
      ▼
 Embeddings (OpenAI/HuggingFace)
      │
      ▼
 ChromaDB (Vector Store)
      │
      ▼
 Retriever (MMR Search)
      │
 User Query ──► LLM (Claude/GPT-4) ──► Answer + Sources
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Anthropic Claude / OpenAI GPT-4 |
| Framework | LangChain 0.2 |
| Vector DB | ChromaDB |
| UI | Streamlit |
| PDF Processing | PyPDF2, pdfplumber |
| Embeddings | OpenAI / HuggingFace |

## Setup

```bash
git clone https://github.com/purnendu1611/medinsight-ai
cd medinsight-ai
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # Add your API keys
streamlit run app.py
```

## Environment Variables

```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here        # optional alternative
LLM_PROVIDER=anthropic              # or "openai"
```

## Usage

1. Launch the app → open `http://localhost:8501`
2. Upload one or more PDF medical reports from the sidebar
3. Click **Process Documents**
4. Type your question in the chat box
5. Get AI-powered answers with source citations

## Example Questions

- *"What is the patient's cholesterol level and is it normal?"*
- *"List all medications mentioned in the report"*
- *"Are there any critical values I should be aware of?"*
- *"Summarize the key findings in simple terms"*
- *"What follow-up tests were recommended?"*

## Project Structure

```
medinsight-ai/
├── app.py                  # Streamlit UI
├── rag_pipeline.py         # Core RAG logic
├── utils/
│   ├── pdf_processor.py    # PDF loading & chunking
│   ├── risk_analyzer.py    # Abnormal value detection
│   └── prompts.py          # LLM prompt templates
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT
