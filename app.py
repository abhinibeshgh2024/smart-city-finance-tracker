from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis import add_financial_metrics, sector_summary, top_overruns
from src.rag import load_project_notes, make_answer, retrieve


BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "smart_city_projects.csv"
NOTES_PATH = BASE_DIR / "data" / "project_notes.txt"


st.set_page_config(
    page_title="Smart City Cost Tracker",
    page_icon="",
    layout="wide",
)

st.title("Smart City Project Cost Tracker")

projects = pd.read_csv(DATA_PATH)
projects = add_financial_metrics(projects)

total_planned = projects["planned_cost_cr"].sum()
total_revised = projects["revised_cost_cr"].sum()
total_spend = projects["actual_spend_cr"].sum()
high_risk_count = int((projects["risk_level"] == "High").sum())

metric_cols = st.columns(4)
metric_cols[0].metric("Planned Cost", f"{total_planned:.1f} cr")
metric_cols[1].metric("Revised Cost", f"{total_revised:.1f} cr")
metric_cols[2].metric("Actual Spend", f"{total_spend:.1f} cr")
metric_cols[3].metric("High Risk Projects", high_risk_count)

tab_dashboard, tab_rag, tab_data = st.tabs(
    ["Cost Dashboard", "RAG Assistant", "Project Data"]
)

with tab_dashboard:
    left, right = st.columns(2)

    with left:
        st.subheader("Sector-wise Revised Cost")
        summary = sector_summary(projects)
        fig = px.bar(
            summary,
            x="sector",
            y="revised_cost_cr",
            color="sector",
            labels={"revised_cost_cr": "Revised Cost (crore)", "sector": "Sector"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Top Cost Overruns")
        overruns = top_overruns(projects)
        fig = px.bar(
            overruns,
            x="project_name",
            y="cost_overrun_pct",
            color="risk_level",
            labels={
                "project_name": "Project",
                "cost_overrun_pct": "Cost Overrun (%)",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Risk Table")
    st.dataframe(
        projects[
            [
                "project_id",
                "project_name",
                "sector",
                "vendor",
                "cost_overrun_pct",
                "delay_months",
                "risk_score",
                "risk_level",
            ]
        ],
        use_container_width=True,
    )

with tab_rag:
    st.subheader("Ask About Project Costs, Delays, and Vendors")
    query = st.text_input(
        "Question",
        value="Which projects have the highest cost escalation and why?",
    )
    top_k = st.slider("Retrieved notes", min_value=1, max_value=5, value=3)

    if query:
        documents = load_project_notes(NOTES_PATH)
        retrieved_docs = retrieve(query, documents, top_k=top_k)
        st.markdown(make_answer(query, retrieved_docs))

        st.subheader("Retrieved Evidence")
        for doc in retrieved_docs:
            st.info(
                f"Source: {doc['source']} | Score: {doc['score']}\n\n{doc['content']}"
            )

with tab_data:
    st.subheader("Full Project Dataset")
    st.dataframe(projects, use_container_width=True)

