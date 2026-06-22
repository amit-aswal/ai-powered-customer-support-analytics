# Phase 3 Data Model Documentation

## Objective

Phase 3 creates the SQL analytics layer for the AI-Powered Customer Support Analytics Platform.

The goal is to convert the cleaned silver dataset into a structured star schema that can support SQL reporting, Power BI dashboards, business KPIs, and analytics engineering workflows.

---

## Data Source

Input dataset:

`data/silver/support_tickets_silver.parquet`

This dataset was created in Phase 2 after cleaning and feature engineering.

---

## Output Database

A local DuckDB analytics database was created:

`data/gold/customer_support_analytics.duckdb`

This database contains the fact and dimension tables used for reporting.

The database is not pushed to GitHub because the data folder is ignored. The database can be recreated by running:

`python src/sql/create_phase3_data_model.py`

---

## Star Schema Design

The Phase 3 model follows a star schema design.

A star schema contains one central fact table and multiple dimension tables.

This approach is commonly used in business intelligence and analytics engineering because it improves query structure, reporting performance, and dashboard usability.

---

## Fact Table

### fact_support_tickets

This is the central table of the model.

It contains one row per support ticket and stores measurable business metrics and foreign keys to dimensions.

Important columns:

| Column | Description |
|---|---|
| ticket_id | Unique ticket identifier |
| created_date_key | Foreign key to dim_date for ticket creation date |
| resolved_date_key | Foreign key to dim_date for resolved date |
| queue_key | Foreign key to dim_queue |
| priority_key | Foreign key to dim_priority |
| language_key | Foreign key to dim_language |
| agent_key | Foreign key to dim_agent |
| category_key | Foreign key to dim_ticket_category |
| status_key | Foreign key to dim_status |
| type_key | Foreign key to dim_type |
| resolution_time_hours | Time taken to resolve closed tickets |
| sla_target_hours | SLA target based on priority |
| combined_text_length | Length of ticket subject and body combined |
| tag_count | Number of tags attached to ticket |
| is_closed | Closed ticket flag |
| is_open | Open ticket flag |
| is_pending | Pending ticket flag |
| is_escalated | Escalated ticket flag |
| is_sla_met | SLA met flag |
| is_sla_breached | SLA breached flag |

---

## Dimension Tables

### dim_date

Stores date-level attributes for created and resolved dates.

Used for:

- Daily trends
- Monthly trends
- Yearly trends
- Weekend analysis

### dim_queue

Stores support queue information.

Used for:

- Queue workload analysis
- Queue performance comparison
- Overloaded team identification

### dim_priority

Stores ticket priority and SLA target information.

Used for:

- Priority distribution
- SLA compliance analysis
- High-priority ticket tracking

### dim_language

Stores customer ticket language.

Used for:

- Language distribution
- Multilingual support analysis

### dim_agent

Stores support agent names.

Used for:

- Agent workload analysis
- Agent SLA breach analysis
- Agent resolution performance

### dim_ticket_category

Stores ticket categories created through rule-based classification.

Used for:

- Complaint category analysis
- Root cause analysis
- Top issue driver reporting

### dim_status

Stores ticket lifecycle status.

Used for:

- Open tickets
- Closed tickets
- Pending tickets
- Escalated tickets

### dim_type

Stores ticket type information.

Used for:

- Ticket type segmentation
- Support request classification

---

## Business KPI Queries Created

The following SQL-based business KPI outputs were created:

| Output File | Business Use |
|---|---|
| executive_kpi_summary.csv | Main executive dashboard KPIs |
| ticket_volume_by_status.csv | Open, closed, pending, escalated ticket split |
| queue_performance.csv | Queue workload and SLA breach analysis |
| priority_sla_performance.csv | SLA compliance by priority |
| agent_performance.csv | Agent workload and performance |
| ticket_category_analysis.csv | Top issue categories |
| monthly_ticket_trend.csv | Monthly ticket volume trend |
| mom_ticket_growth.csv | Month-over-month ticket growth |
| language_distribution.csv | Ticket distribution by language |
| top_sla_breach_drivers.csv | Top SLA breach drivers by queue, category, and priority |

---

## SQL Concepts Used

Phase 3 uses:

- Joins
- Aggregations
- CTEs
- Window functions
- RANK
- LAG
- CASE WHEN
- Date extraction
- Star schema modeling
- Fact and dimension table design

---

## Validation

The model was validated using:

- Fact table row count check
- Unique ticket ID check
- Missing foreign key check
- Table row count report
- Queue performance validation
- Category performance validation

Important validation outputs:

- `reports/phase3/phase3_table_row_counts.csv`
- `reports/phase3/phase3_fact_validation.csv`
- `reports/phase3/phase3_sql_data_model_report.md`

---

## Business Value

The Phase 3 SQL model makes the data ready for Power BI and business reporting.

It enables management to answer:

- How many tickets were received?
- How many tickets are open?
- What is the average resolution time?
- Which queues are overloaded?
- Which priorities breach SLA?
- Which agents have the highest workload?
- Which complaint categories are most common?
- What is the monthly ticket trend?
- What are the top SLA breach drivers?

---

## Important Note

Some operational fields used in this model were simulated in Phase 2 because the original dataset does not include real ticket lifecycle data.

These fields are clearly marked using:

`is_operational_data_simulated = True`

This keeps the project transparent and honest.
