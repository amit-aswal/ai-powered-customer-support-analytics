# Project Architecture

## Project Name

AI-Powered Customer Support Analytics Platform

---

## Architecture Overview

The project follows a layered analytics architecture.

```text
Raw Dataset
    ?
Bronze Layer
    ?
Silver Layer
    ?
Gold Layer
    ?
Business KPI Reports
    ?
Power BI Dashboard
    ?
NLP and AI Summary
Bronze Layer

The bronze layer stores raw customer support ticket data.

Purpose:

Preserve original data
Store raw CSV and Parquet files
Avoid modifying source data directly

Main file:

data/bronze/support_tickets_raw.parquet

Silver Layer

The silver layer stores cleaned and feature-engineered data.

Purpose:

Clean text fields
Standardize columns
Create ticket ID
Add operational fields
Create SLA and status fields
Create rule-based ticket categories

Main file:

data/silver/support_tickets_silver.parquet

Gold Layer

The gold layer stores analytics-ready datasets.

Purpose:

DuckDB SQL model
Fact and dimension tables
Power BI exports
Text analytics outputs

Main database:

data/gold/customer_support_analytics.duckdb

SQL Model

The SQL model follows a star schema.

Fact table:

fact_support_tickets

Dimension tables:

dim_date
dim_queue
dim_priority
dim_language
dim_agent
dim_ticket_category
dim_status
dim_type
Dashboard Layer

Power BI dashboard contains 6 pages:

Executive Overview
Queue Performance
SLA Performance
Agent Workload
Ticket Category Analysis
Monthly Trend Analysis
NLP Layer

The NLP layer creates:

Sentiment score
Sentiment label
Urgency score
Urgency label
Keyword extraction
Negative ticket samples
Reporting Layer

The reporting layer creates:

Business recommendations
AI-style executive summary
Final project business impact report
Business Outcome

The architecture converts raw support tickets into business-ready insights for support operations, management reporting, and decision-making.
