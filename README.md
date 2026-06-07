# Smart City Project Cost Tracker

A RAG-based data science starter project for tracking smart city project costs, delays, vendors, and financial risk.

## Project Goal

This project helps users ask questions about smart city infrastructure projects such as:

- Which projects have cost overruns?
- Which vendors are linked to delayed projects?
- What is the revised cost of the smart parking project?
- Which projects are high financial risk?
- Summarize spending by sector.

## Features

- Project cost dataset analysis
- Planned vs revised vs actual cost tracking
- Cost overrun percentage calculation
- Delay and risk scoring
- Simple retrieval-based Q&A over project notes
- Streamlit dashboard starter app

## Folder Structure

```text
smart_city_cost_tracker/
  app.py
  requirements.txt
  data/
    smart_city_projects.csv
    project_notes.txt
  src/
    analysis.py
    rag.py
```

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run app.py
```

## Deploy On Streamlit Community Cloud

1. Push this project folder to a GitHub repository.
2. Go to https://share.streamlit.io/.
3. Create a new app.
4. Select the GitHub repository.
5. Set the main file path to:

```text
app.py
```

6. Deploy the app.

Streamlit Cloud will install dependencies from `requirements.txt`.

## Suggested Dataset Columns

- project_id
- project_name
- sector
- ward
- vendor
- planned_cost_cr
- revised_cost_cr
- actual_spend_cr
- planned_duration_months
- actual_duration_months
- status
- funding_source
- notes

## Data Science Extensions

- Cost overrun prediction
- Vendor concentration analysis
- Delay classification
- Project financial risk score
- Sector-wise budget visualization
- RAG answers with citations from tenders, DPRs, budgets, and progress reports
