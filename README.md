# AI-Powered Customer Support Analytics Platform

## Project Overview

This project is an end-to-end customer support analytics platform built using Python, SQL, DuckDB, Power BI, and NLP.

The project uses a customer support ticket dataset with more than 61,000 tickets and converts raw ticket data into business-ready insights, SQL models, Power BI dashboards, sentiment analysis, urgency scoring, and AI-style executive recommendations.

The goal is to simulate how a real company can analyze support tickets to understand workload, SLA performance, queue bottlenecks, agent workload, customer issue categories, and text-based customer concerns.

---

## Business Problem

Customer support teams receive thousands of tickets across different queues, priorities, agents, and issue categories.

Without an analytics system, support leaders may struggle to answer:

* How many tickets are open, closed, pending, or escalated?
* Which support queues are overloaded?
* Which priorities breach SLA most often?
* Which agents have the highest workload?
* What are customers complaining about most?
* Are negative or urgent tickets increasing?
* Which business areas need immediate attention?

This project solves this problem by creating a complete analytics workflow from raw ticket data to dashboard and executive recommendations.

---

## Project Goal

The goal of this project is to build a complete analytics system that can:

* Ingest raw customer support ticket data
* Profile and validate data quality
* Clean and engineer business-ready fields
* Create SQL-based fact and dimension tables
* Generate business KPI reports
* Build Power BI dashboards
* Perform NLP sentiment and urgency analysis
* Generate executive summaries and business recommendations

---

## Tech Stack

| Area                  | Tools Used                                                |
| --------------------- | --------------------------------------------------------- |
| Programming           | Python                                                    |
| Data Processing       | Pandas, NumPy                                             |
| Data Source           | Hugging Face Dataset                                      |
| Storage               | CSV, Parquet                                              |
| SQL Engine            | DuckDB                                                    |
| Data Modeling         | Star Schema, Fact and Dimension Tables                    |
| Business Intelligence | Power BI                                                  |
| NLP                   | Rule-based Sentiment, Urgency Scoring, Keyword Extraction |
| Visualization         | Matplotlib, Power BI                                      |
| Version Control       | Git, GitHub                                               |
| Documentation         | Markdown                                                  |

---

## Project Architecture

```text
Raw Hugging Face Dataset
        ↓
Bronze Layer
Raw ticket data stored as CSV and Parquet
        ↓
Silver Layer
Cleaned and feature-engineered ticket data
        ↓
Gold Layer
DuckDB SQL model and Power BI exports
        ↓
Business KPI Reports
SQL-based operational metrics
        ↓
EDA and Business Insights
Charts, summaries, and recommendations
        ↓
Power BI Dashboard
Executive and operational reporting
        ↓
NLP Layer
Sentiment, urgency, and keyword analysis
        ↓
AI Executive Summary
Final business recommendations
```

---

## Completed Project Phases

### Phase 1: Data Understanding and Profiling

* Loaded customer support ticket dataset from Hugging Face
* Stored raw data in the bronze layer
* Created missing value, duplicate, categorical, and text length reports
* Identified important business data gaps

Important files:

* `src/ingestion/load_huggingface_dataset.py`
* `src/profiling/profile_raw_tickets.py`
* `reports/phase1_data_profile_report.md`

---

### Phase 2: Data Cleaning and Feature Engineering

* Cleaned ticket text fields
* Created unique ticket IDs
* Created status, created date, resolved date, resolution time, SLA status, and agent name
* Created rule-based ticket categories
* Created validation reports
* Documented simulated fields clearly

Important files:

* `src/features/feature_engineering.py`
* `src/features/validate_phase2_data.py`
* `docs/phase2_data_dictionary.md`
* `reports/phase2/`

---

### Phase 3: SQL Data Model and Analytics Layer

Created a DuckDB-based SQL analytics model using a star schema.

Fact table:

* `fact_support_tickets`

Dimension tables:

* `dim_date`
* `dim_queue`
* `dim_priority`
* `dim_language`
* `dim_agent`
* `dim_ticket_category`
* `dim_status`
* `dim_type`

Important files:

* `src/sql/create_phase3_data_model.py`
* `src/sql/run_phase3_business_kpis.py`
* `sql/analytics/phase3_business_kpi_queries.sql`
* `docs/phase3_data_model_documentation.md`
* `reports/phase3/`

---

### Phase 4: EDA and Business Insights

* Created executive KPI summary
* Analyzed queue workload
* Analyzed SLA breaches
* Analyzed ticket categories
* Analyzed agent workload
* Created monthly trend analysis
* Created business recommendations

Important files:

* `src/eda/run_phase4_eda.py`
* `reports/phase4/phase4_eda_business_insights_report.md`
* `reports/phase4/charts/`

---

### Phase 5: Power BI Dataset Preparation

* Created dashboard-ready Power BI exports
* Created KPI summary files
* Created dashboard planning documentation
* Created Power BI DAX measure reference

Important files:

* `src/dashboard/prepare_phase5_powerbi_dataset.py`
* `reports/phase5/phase5_powerbi_dashboard_plan.md`
* `reports/phase5/phase5_powerbi_measure_reference.md`

---

### Phase 6: Power BI Dashboard

Built a complete Power BI dashboard with 6 pages:

1. Executive Overview
2. Queue Performance
3. SLA Performance
4. Agent Workload
5. Ticket Category Analysis
6. Monthly Trend Analysis

Important files:

* `dashboards/powerbi/customer_support_analytics_dashboard.pbix`
* `docs/phase6_powerbi_dashboard_build_guide.md`
* `reports/phase6/screenshots/`
* `reports/phase6/phase6_powerbi_dashboard_report.md`

---

### Phase 7: NLP and Text Analytics

* Created cleaned NLP text
* Created sentiment scores and sentiment labels
* Created urgency scores and urgency labels
* Extracted top keywords
* Identified negative tickets
* Created sentiment by category and queue
* Created urgency by priority

Important files:

* `src/nlp/run_phase7_text_analytics.py`
* `reports/phase7/phase7_nlp_text_analytics_report.md`
* `reports/phase7/charts/`

---

### Phase 8: AI Executive Summary and Recommendations

* Combined EDA outputs and NLP outputs
* Created AI-style executive summary
* Created final business recommendations
* Created final business impact report

Important files:

* `src/reporting/generate_phase8_executive_summary.py`
* `reports/phase8/phase8_ai_executive_summary.md`
* `reports/phase8/phase8_business_recommendations.csv`
* `reports/phase8/final_project_business_impact_report.md`

---

## Power BI Dashboard Preview

Dashboard screenshots are stored in:

`reports/phase6/screenshots/`

Screenshots included:

* Executive Overview
* Queue Performance
* SLA Performance
* Agent Workload
* Ticket Category Analysis
* Monthly Trend Analysis

---

## Key Business KPIs

The project tracks:

* Total tickets
* Open tickets
* Closed tickets
* Pending tickets
* Escalated tickets
* Average resolution time
* SLA met tickets
* SLA breached tickets
* SLA compliance percentage
* SLA breach percentage
* Queue workload
* Agent workload
* Ticket category distribution
* Monthly ticket trends
* Sentiment distribution
* Urgency distribution

---

## Business Value

This project helps support leaders:

* Monitor customer support workload
* Identify overloaded queues
* Track SLA performance
* Find recurring customer issue categories
* Analyze agent workload
* Detect negative and urgent tickets
* Understand monthly ticket trends
* Generate management-ready recommendations
* Reduce manual reporting effort

---

## How to Run the Project

### 1. Create and activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run data ingestion

```powershell
python src/ingestion/load_huggingface_dataset.py
```

### 4. Run raw data profiling

```powershell
python src/profiling/profile_raw_tickets.py
```

### 5. Run feature engineering

```powershell
python src/features/feature_engineering.py
```

### 6. Run Phase 2 validation

```powershell
python src/features/validate_phase2_data.py
```

### 7. Create SQL data model

```powershell
python src/sql/create_phase3_data_model.py
```

### 8. Run business KPI queries

```powershell
python src/sql/run_phase3_business_kpis.py
```

### 9. Run EDA and business insights

```powershell
python src/eda/run_phase4_eda.py
```

### 10. Prepare Power BI dataset

```powershell
python src/dashboard/prepare_phase5_powerbi_dataset.py
```

### 11. Run NLP and text analytics

```powershell
python src/nlp/run_phase7_text_analytics.py
```

### 12. Generate executive summary

```powershell
python src/reporting/generate_phase8_executive_summary.py
```

---

## Important Data Note

The original dataset does not include operational lifecycle fields such as ticket status, created date, resolved date, resolution time, agent name, and SLA status.

These fields were simulated in Phase 2 using documented logic to demonstrate how a real customer support analytics workflow would operate.

The original raw data is preserved separately in the bronze layer.

---

## Repository Structure

```text
data/
  bronze/
  silver/
  gold/

src/
  ingestion/
  profiling/
  features/
  sql/
  eda/
  dashboard/
  nlp/
  reporting/

sql/
  analytics/
  profiling/

reports/
  phase2/
  phase3/
  phase4/
  phase5/
  phase6/
  phase7/
  phase8/

docs/
dashboards/
```

---

## Skills Demonstrated

* Python scripting
* Data ingestion
* Data profiling
* Data cleaning
* Feature engineering
* Data validation
* SQL analytics
* DuckDB data modeling
* Star schema design
* KPI reporting
* EDA and business insights
* Power BI dashboarding
* DAX measures
* NLP sentiment analysis
* Urgency scoring
* Keyword extraction
* Executive reporting
* Git and GitHub workflow

---

## Resume Summary

Built an end-to-end AI-powered customer support analytics platform using Python, SQL, DuckDB, Power BI, and NLP to analyze 61K+ support tickets and generate business KPIs, dashboards, sentiment insights, urgency scores, and executive recommendations.

---

## Project Status

Completed:

* Data ingestion
* Data profiling
* Feature engineering
* Data validation
* SQL model
* Business KPI reports
* EDA insights
* Power BI dashboard
* NLP text analytics
* AI-style executive summary
* Final business recommendations

---

## Future Improvements

Possible future enhancements:

* Add Streamlit web application
* Allow CSV upload for dynamic analysis
* Add transformer-based sentiment analysis
* Add LLM-powered ticket summarization
* Add automated PDF executive reports
* Add database refresh automation
* Deploy dashboard and app online

---

### Phase 10: Streamlit Web App

Created an interactive Streamlit web app to present the final project outputs in a browser.

Key work:

- Built a multi-page Streamlit app
- Added executive KPI view
- Added queue, SLA, agent, category, and monthly trend pages
- Added NLP sentiment and urgency insights
- Added business recommendations page
- Added AI executive summary page
- Added project overview page

Important files:

- `app/streamlit_app.py`
- `docs/phase10_streamlit_app.md`

Run command:

`streamlit run app/streamlit_app.py`

Business value:

The Streamlit app makes the project easier to present because recruiters and reviewers can view the final analytics outputs through one interactive browser interface.
