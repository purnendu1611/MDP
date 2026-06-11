# Data Analyst Agent

I work a lot with CSV/Excel data and I'm tired of writing the same Pandas boilerplate over and over. This is my attempt at a "just ask the data" tool — upload any dataset, ask a question in plain English, and get a chart + a plain-English explanation back.

The interesting part is the multi-agent setup. There's a separate agent for writing the Pandas code, one for deciding what chart to make, and one for narrating the findings. They're all just GPT-4o calls but keeping them separate made the whole thing way more reliable than one giant prompt.

---

## What it does

- Upload a CSV or Excel file
- Ask anything: *"Which region had the highest sales last quarter?"*, *"Show me outliers in the age column"*, *"What correlates most with churn?"*
- Get back: the generated Pandas code + a chart + a 3-sentence insight
- Auto EDA tab — one click to get missing values, distributions, correlations for any dataset

## Tech

- Python, Streamlit
- OpenAI GPT-4o (analysis) + GPT-4o-mini (charts, narration)
- Pandas, Plotly
- Multi-agent orchestration (custom, no framework overhead)

## Setup

```bash
git clone https://github.com/purnendu1611/data-analyst-agent
cd data-analyst-agent

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env    # add OPENAI_API_KEY

streamlit run app.py
```

## Project layout

```
data-analyst-agent/
├── app.py                  # Streamlit UI
├── orchestrator.py         # routes queries to the right agent
├── agents/
│   ├── data_analyst.py     # generates + runs Pandas code
│   ├── chart_generator.py  # picks chart type + builds Plotly figure
│   ├── narrator.py         # plain-English explanation of results
│   └── statistics_agent.py # EDA, outlier detection
├── utils/
│   └── data_loader.py
└── requirements.txt
```

## Example queries

Works well on most tabular datasets. I've tested it on the hospital analytics and diabetes datasets from my other projects:

- *"What's the average glucose level by age group?"*
- *"Show the distribution of BMI"*
- *"Which features correlate most with the target variable?"*
- *"How many missing values are there per column?"*

## Known limitations

- Only works with CSV and Excel right now — no SQL databases yet
- Very wide tables (100+ columns) confuse the chart agent sometimes
- Generated code runs in-process, so if your CSV is 10M rows it'll be slow

## TODO

- [ ] Add SQL database connector
- [ ] Let users download the generated code as a .py file
- [ ] Memory across questions (right now each query is stateless)
- [ ] Better handling of datetime columns
