# 📊 Data Analyst Agent — Multi-Agent AI for Automated Data Analysis

> Upload any CSV or Excel file, ask questions in plain English, and get instant charts, statistics, and business insights — powered by a multi-agent LLM system.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![LangChain](https://img.shields.io/badge/LangChain-0.2-green) ![Plotly](https://img.shields.io/badge/Plotly-5.x-cyan) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)

---

## Features

- **Natural Language Queries** — *"Show me sales by region as a bar chart"*
- **Auto EDA** — automated exploratory data analysis report
- **Smart Visualizations** — bar, line, scatter, heatmap, histogram selected by context
- **Statistical Analysis** — correlation, outlier detection, distribution analysis
- **Multi-Agent System** — specialized agents for different tasks (planning, coding, validation, narration)
- **Code Transparency** — see the Python/Pandas code generated for every answer
- **Export Reports** — download full analysis as HTML/PDF

## Multi-Agent Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                  Orchestrator Agent                  │
│         (plans tasks, routes to sub-agents)          │
└────┬──────────────┬─────────────────┬───────────────┘
     │              │                 │
     ▼              ▼                 ▼
┌─────────┐  ┌───────────┐   ┌──────────────┐
│  Data   │  │  Chart    │   │  Statistics  │
│Analyst  │  │ Generator │   │    Agent     │
│ Agent   │  │  Agent    │   │              │
└────┬────┘  └─────┬─────┘   └──────┬───────┘
     │              │                │
     └──────────────┴────────────────┘
                    │
                    ▼
          ┌─────────────────┐
          │ Narrator Agent  │
          │ (plain English  │
          │  explanation)   │
          └─────────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | OpenAI GPT-4o / GPT-4o-mini |
| Agent Framework | LangChain Agents + custom orchestrator |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib |
| UI | Streamlit |
| Code Execution | Python sandbox (RestrictedPython) |

## Setup

```bash
git clone https://github.com/purnendu1611/data-analyst-agent
cd data-analyst-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## Example Queries

Given a sales dataset:

| Query | What the agent does |
|-------|---------------------|
| *"What's the total revenue by region?"* | Groups by region, sums revenue, creates bar chart |
| *"Are there any outliers in the data?"* | IQR analysis, Z-score, box plot |
| *"Show the trend of sales over the last 12 months"* | Time series line chart with moving average |
| *"Which product has the highest return rate?"* | Aggregation + ranked table |
| *"Summarize this dataset for me"* | Full EDA: shape, dtypes, missing values, statistics |
| *"What factors correlate most with customer churn?"* | Correlation heatmap + top factors |

## Project Structure

```
data-analyst-agent/
├── app.py                      # Streamlit UI
├── orchestrator.py             # Master agent (plans & routes)
├── agents/
│   ├── data_analyst.py         # Pandas operations agent
│   ├── chart_generator.py      # Plotly chart agent
│   ├── statistics_agent.py     # Statistical analysis agent
│   └── narrator.py             # Plain-English explanation agent
├── utils/
│   ├── data_loader.py          # CSV/Excel loading & validation
│   ├── code_executor.py        # Safe Python code runner
│   └── prompts.py              # Prompt templates per agent
├── requirements.txt
├── .env.example
└── README.md
```

## Sample Output

```
User: "Which age group has the highest diabetes risk in this dataset?"

Agent Plan:
  1. [DataAnalyst] Group by age_group, calculate diabetes_rate
  2. [Statistics] Run chi-square test for significance
  3. [ChartGenerator] Create grouped bar chart
  4. [Narrator] Explain findings in plain English

Result:
  - Age group 60-70 shows highest risk (34.2%)
  - Statistically significant (p < 0.001)
  - Chart: [interactive bar chart]
  - "Patients aged 60-70 are 2.4x more likely to have diabetes
     compared to the 20-30 age group. This aligns with clinical
     literature. Recommend targeted screening for this cohort."
```

## License

MIT
