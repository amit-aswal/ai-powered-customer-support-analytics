# Phase 10 Streamlit Web App

## Objective

Phase 10 adds an interactive Streamlit web app to the AI-Powered Customer Support Analytics Platform.

The app allows users and recruiters to view project outputs in a browser without opening multiple CSV files or reports manually.

---

## App File

`app/streamlit_app.py`

---

## How to Run

```powershell
streamlit run app/streamlit_app.py
After running the command, the app opens locally at:

http://localhost:8501

App Pages

The Streamlit app includes the following pages:

Executive Overview
Queue Performance
SLA Performance
Agent Workload
Ticket Category Analysis
Monthly Trend Analysis
NLP Insights
Business Recommendations
AI Executive Summary
About Project
Data Used

The app reads already generated project outputs from:

reports/phase4/
reports/phase7/
reports/phase8/

It does not require the large raw dataset to be pushed to GitHub.

Business Value

The Streamlit app makes the project easier to present because it gives a single interactive interface for:

Executive KPIs
Ticket status analysis
Queue workload analysis
SLA performance tracking
Agent workload review
Ticket category analysis
Monthly ticket trend analysis
Sentiment analysis
Urgency analysis
Business recommendations
Recruiter Value

Recruiters can quickly understand the project by running one command and viewing the final analytics outputs in a browser.

This makes the project more interactive and portfolio-friendly.
