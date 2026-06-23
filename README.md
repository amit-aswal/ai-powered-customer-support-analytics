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


---

## Phase 3: SQL Data Model and Analytics Layer

Phase 3 converts the cleaned silver dataset into a SQL-based analytics model using DuckDB.

### Objective

The objective of Phase 3 is to design a business-ready star schema that supports executive KPIs, operational reporting, Power BI dashboards, and analytics engineering workflows.

### Data Model

The model follows a star schema design with one central fact table and multiple dimension tables.

### Fact Table

- `fact_support_tickets`

### Dimension Tables

- `dim_date`
- `dim_queue`
- `dim_priority`
- `dim_language`
- `dim_agent`
- `dim_ticket_category`
- `dim_status`
- `dim_type`

### Tools Used

- DuckDB
- SQL
- Python
- Pandas
- Parquet

### Key Activities

- Loaded the silver dataset into DuckDB
- Created date, queue, priority, language, agent, category, status, and type dimensions
- Created the central support ticket fact table
- Added foreign keys from fact table to dimension tables
- Created KPI-ready flags such as is_open, is_closed, is_sla_met, and is_sla_breached
- Generated SQL validation reports
- Created business KPI query outputs

### Business KPI Outputs

- `reports/phase3/business_kpis/executive_kpi_summary.csv`
- `reports/phase3/business_kpis/ticket_volume_by_status.csv`
- `reports/phase3/business_kpis/queue_performance.csv`
- `reports/phase3/business_kpis/priority_sla_performance.csv`
- `reports/phase3/business_kpis/agent_performance.csv`
- `reports/phase3/business_kpis/ticket_category_analysis.csv`
- `reports/phase3/business_kpis/monthly_ticket_trend.csv`
- `reports/phase3/business_kpis/mom_ticket_growth.csv`
- `reports/phase3/business_kpis/language_distribution.csv`
- `reports/phase3/business_kpis/top_sla_breach_drivers.csv`

### SQL Scripts

- `sql/analytics/phase3_business_kpi_queries.sql`

### Python Scripts

- `src/sql/create_phase3_data_model.py`
- `src/sql/run_phase3_business_kpis.py`

### Documentation

- `docs/phase3_data_model_documentation.md`
- `reports/phase3/phase3_sql_data_model_report.md`

### Business Value

After Phase 3, the project has a proper SQL analytics layer that supports:

- Executive KPI reporting
- Queue workload analysis
- SLA compliance monitoring
- Agent performance reporting
- Ticket category analysis
- Monthly trend analysis
- Power BI dashboard preparation

### Important Note

The DuckDB database is created locally at:

`data/gold/customer_support_analytics.duckdb`

The database is not pushed to GitHub because the data folder is ignored. It can be recreated by running:

`python src/sql/create_phase3_data_model.py`

---

## Phase 4: Exploratory Data Analysis and Business Insights

Phase 4 converts the SQL analytics model into business insights, charts, and recommendations.

### Objective

The objective of Phase 4 is to analyze ticket volume, SLA performance, queue workload, ticket categories, agent workload, and monthly trends.

### Key Activities

- Generated executive KPI summary
- Analyzed ticket status distribution
- Identified high-volume support queues
- Analyzed SLA breaches by priority
- Compared agent workload
- Identified top ticket categories
- Created monthly ticket trend analysis
- Created month-over-month growth analysis
- Identified top SLA breach drivers
- Created business recommendations

### Phase 4 Outputs

CSV reports were generated in:

`reports/phase4/`

Charts were generated in:

`reports/phase4/charts/`

Main insight report:

`reports/phase4/phase4_eda_business_insights_report.md`

### Charts Created

- Ticket volume by status
- Top 10 queues by ticket volume
- Ticket volume by category
- Monthly ticket volume trend
- SLA breaches by priority
- Top 10 agents by workload

### Business Value

Phase 4 helps support leadership understand:

- How many tickets are being handled
- Which queues have the highest workload
- Which categories create the most support demand
- Which priority groups breach SLA most often
- Which agents have the highest workload
- Which months have the highest ticket volume
- Which operational areas need attention

### Important Note

Some operational fields used in the analysis were simulated in Phase 2 because the original dataset does not include real lifecycle fields such as ticket status, created date, resolved date, agent name, and SLA status.

These fields are clearly documented as simulated fields.

---

## Phase 5: Power BI Dashboard Dataset Preparation

Phase 5 prepares the project for Power BI dashboard development.

### Objective

The objective of Phase 5 is to create dashboard-ready CSV files, KPI summary tables, Power BI measure references, and dashboard planning documentation.

### Key Activities

- Created a dashboard-ready fact table for Power BI
- Created KPI summary exports
- Created queue performance dashboard data
- Created SLA performance dashboard data
- Created agent workload dashboard data
- Created ticket category dashboard data
- Created monthly trend dashboard data
- Created Power BI DAX measure reference
- Created dashboard page planning documentation

### Power BI Export Folder

Dashboard-ready files are created locally in:

`data/gold/powerbi_exports/`

Important files:

- `powerbi_fact_support_tickets_dashboard.csv`
- `powerbi_kpi_summary.csv`
- `powerbi_status_summary.csv`
- `powerbi_queue_summary.csv`
- `powerbi_priority_summary.csv`
- `powerbi_agent_summary.csv`
- `powerbi_category_summary.csv`
- `powerbi_monthly_summary.csv`
- `powerbi_top_sla_breach_drivers.csv`

### GitHub Report Files

Preview summary files and documentation are stored in:

`reports/phase5/`

### Documentation

- `reports/phase5/phase5_powerbi_dashboard_plan.md`
- `reports/phase5/phase5_powerbi_measure_reference.md`
- `reports/phase5/phase5_dashboard_dataset_preparation_report.md`

### Business Value

Phase 5 prepares the analytics layer for a business-facing dashboard that can help support leaders track:

- Ticket volume
- Open and closed tickets
- SLA compliance
- Queue workload
- Agent workload
- Ticket categories
- Monthly ticket trends
- SLA breach drivers

### Important Note

The main Power BI fact export is saved locally inside the ignored data folder and is not pushed to GitHub. The script can recreate it anytime by running:

`python src/dashboard/prepare_phase5_powerbi_dataset.py`

---

## Phase 6: Power BI Dashboard

Phase 6 builds the Power BI dashboard for the AI-Powered Customer Support Analytics Platform.

### Objective

The objective of Phase 6 is to convert the dashboard-ready dataset into a business-facing Power BI report for support operations monitoring.

### Dashboard File

The Power BI dashboard is saved at:

`dashboards/powerbi/customer_support_analytics_dashboard.pbix`

### Dashboard Pages

The dashboard contains 6 pages:

- Executive Overview
- Queue Performance
- SLA Performance
- Agent Workload
- Ticket Category Analysis
- Monthly Trend Analysis

### Key Metrics

The dashboard tracks:

- Total Tickets
- Open Tickets
- Closed Tickets
- Pending Tickets
- Escalated Tickets
- Average Resolution Time
- SLA Met Tickets
- SLA Breached Tickets
- SLA Compliance %
- SLA Breach %

### Dashboard Screenshots

Dashboard screenshots are stored in:

`reports/phase6/screenshots/`

### Documentation

- `docs/phase6_powerbi_dashboard_build_guide.md`
- `reports/phase6/phase6_powerbi_dax_measures.md`
- `reports/phase6/phase6_powerbi_dashboard_report.md`

### Business Value

The dashboard helps support leaders understand:

- Overall support workload
- Queue-level workload
- SLA compliance and breach risk
- Agent workload distribution
- Most common ticket categories
- Monthly support trends

### Important Note

Some operational fields used in the dashboard were simulated in Phase 2 because the original dataset does not include real ticket lifecycle fields. These fields are clearly documented as simulated.
