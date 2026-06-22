# AI-Powered Customer Support Analytics Platform

## Project Overview

This project is an end-to-end analytics and AI solution for customer support operations.

Customer support teams receive thousands of tickets every day. Management needs visibility into ticket volume, support queues, customer sentiment, recurring complaints, SLA performance, and operational bottlenecks.

This project uses SQL, Python, NLP, Generative AI, Power BI, Streamlit, and automation to convert raw support ticket data into business insights.

## Dataset

The dataset used in this project is the Hugging Face Customer Support Tickets dataset:

`Tobi-Bueck/customer-support-tickets`

The dataset contains 61,765 customer support ticket records and 16 raw columns.

Raw columns include:

- subject
- body
- answer
- type
- queue
- priority
- language
- version
- tag_1 to tag_8

## Phase 1: Data Understanding and Data Profiling

The first phase focuses on understanding the raw customer support tickets dataset before applying cleaning, SQL modeling, NLP, AI, or dashboarding.

### Key Activities

- Loaded raw customer support ticket data from Hugging Face
- Stored the original dataset in the bronze layer
- Created column-level profiling report
- Analyzed missing values
- Checked possible duplicate tickets
- Analyzed ticket distribution by type, queue, priority, and language
- Profiled subject, body, and answer text length
- Identified missing operational business fields
- Created SQL profiling outputs using DuckDB

### Business Value

This phase ensures that all downstream analytics, dashboards, SQL metrics, and AI summaries are built on a clear understanding of the raw data.

It also identifies which fields need to be engineered later for enterprise support analytics.

### Key Finding

The dataset is strong for ticket classification, support queue analysis, NLP, sentiment analysis, root cause analysis, and AI summarization.

However, it does not include enterprise operational fields such as:

- ticket_id
- created_date
- resolved_date
- status
- agent_name
- resolution_time_hours
- sla_status
- sentiment
- ticket_category

These fields will be engineered in Phase 2.

## Phase 1 Outputs

### Bronze Layer

- `data/bronze/support_tickets_raw.parquet`
- `data/bronze/support_tickets_raw.csv`

### Python Profiling Reports

- `reports/column_profile.csv`
- `reports/missing_values_report.csv`
- `reports/categorical_distribution_report.csv`
- `reports/text_length_profile.csv`
- `reports/duplicate_report.csv`
- `reports/business_gap_report.csv`
- `reports/phase1_data_profile_report.md`

### SQL Profiling Outputs

- `reports/sql_outputs/sql_total_tickets.csv`
- `reports/sql_outputs/sql_type_distribution.csv`
- `reports/sql_outputs/sql_queue_distribution.csv`
- `reports/sql_outputs/sql_priority_distribution.csv`
- `reports/sql_outputs/sql_language_distribution.csv`
- `reports/sql_outputs/sql_queue_priority_matrix.csv`
- `reports/sql_outputs/sql_missing_text_fields.csv`
- `reports/sql_outputs/sql_text_length_profile.csv`
- `reports/sql_outputs/sql_top_queues_ranked.csv`

## Tools Used in Phase 1

- Python
- Pandas
- Hugging Face Datasets
- PyArrow
- DuckDB
- SQL
- VS Code

## Next Phase

Phase 2 will focus on Data Cleaning and Feature Engineering.

In Phase 2, the project will create business-ready fields such as:

- ticket_id
- status
- created_date
- resolved_date
- resolution_time_hours
- agent_name
- sla_status
- cleaned_ticket_text

---

## Phase 2: Data Cleaning and Feature Engineering

Phase 2 converts the raw bronze support ticket dataset into a cleaned and business-ready silver dataset.

### Objective

The objective of Phase 2 is to prepare the raw customer support ticket data for SQL modeling, KPI calculation, Power BI dashboarding, Streamlit app development, and future NLP/AI analysis.

### Key Activities

- Loaded raw data from the bronze layer
- Standardized column names
- Cleaned text fields such as subject, body, and answer
- Created unique ticket IDs
- Created cleaned categorical fields
- Simulated ticket lifecycle fields
- Simulated created and resolved dates
- Calculated resolution time
- Assigned simulated support agents
- Created SLA targets and SLA status
- Combined tag columns
- Created rule-based ticket categories
- Created data quality flags
- Created validation checks for Phase 2

### Silver Layer Outputs

- `data/silver/support_tickets_silver.parquet`
- `data/silver/support_tickets_silver.csv`

### Phase 2 Reports

- `reports/phase2/phase2_feature_engineering_report.md`
- `reports/phase2/phase2_feature_engineering_summary.csv`
- `reports/phase2/phase2_status_distribution.csv`
- `reports/phase2/phase2_sla_distribution.csv`
- `reports/phase2/phase2_ticket_category_distribution.csv`
- `reports/phase2/phase2_data_validation_report.csv`
- `reports/phase2/phase2_data_validation_report.md`

### Data Dictionary

- `docs/phase2_data_dictionary.md`

### Important Note on Synthetic Fields

The original dataset does not include operational fields such as ticket status, created date, resolved date, resolution time, assigned agent, or SLA status.

These fields were engineered using reproducible simulation logic to create a realistic enterprise analytics environment.

They are clearly flagged using:

`is_operational_data_simulated = True`

### Business Value

After Phase 2, the dataset can support business questions such as:

- How many tickets are open, closed, pending, or escalated?
- What is the average resolution time?
- Which tickets breached SLA?
- Which support agents have more workload?
- Which ticket categories are most common?
- Which queues require operational attention?

### Validation

Phase 2 includes validation checks to ensure:

- No rows were lost
- Original raw columns were preserved
- Original raw values were unchanged
- Ticket IDs are unique
- Date logic is valid
- SLA logic is valid
- Synthetic fields are clearly documented

