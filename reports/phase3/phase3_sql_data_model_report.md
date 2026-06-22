# Phase 3 SQL Data Model Report

## Objective

Phase 3 creates a SQL analytics model from the cleaned silver customer support ticket dataset.

The purpose of this phase is to convert the flat silver dataset into a star schema that can support SQL analytics, Power BI dashboards, and business KPI reporting.

## Data Model Type

This phase uses a star schema.

A star schema has one central fact table and multiple dimension tables.

## Fact Table

- fact_support_tickets

## Dimension Tables

- dim_date
- dim_queue
- dim_priority
- dim_language
- dim_agent
- dim_ticket_category
- dim_status
- dim_type

## Table Row Counts

| table_name           |   row_count |
|:---------------------|------------:|
| fact_support_tickets |       61765 |
| dim_date             |         554 |
| dim_queue            |          52 |
| dim_priority         |           5 |
| dim_language         |           2 |
| dim_agent            |          12 |
| dim_ticket_category  |           8 |
| dim_status           |           4 |
| dim_type             |           5 |

## Fact Table Validation

|   total_fact_rows |   unique_ticket_ids |   duplicate_ticket_ids |   missing_created_date_key |   missing_queue_key |   missing_priority_key |   missing_language_key |   missing_agent_key |   missing_category_key |   missing_status_key |   missing_type_key |
|------------------:|--------------------:|-----------------------:|---------------------------:|--------------------:|-----------------------:|-----------------------:|--------------------:|-----------------------:|---------------------:|-------------------:|
|             61765 |               61765 |                      0 |                          0 |                   0 |                      0 |                      0 |                   0 |                      0 |                    0 |                  0 |

## Business Value

The Phase 3 model makes the dataset ready for analytics and dashboarding.

It enables business users to analyze:

- Ticket volume
- Open and closed tickets
- Queue workload
- Priority distribution
- SLA compliance
- Agent performance
- Ticket category trends
- Resolution time metrics
- Monthly support trends

## Important Note

The operational fields used in this model, such as status, created_date, resolved_date, resolution_time_hours, agent_name, and SLA status, were engineered in Phase 2 using documented simulation logic.

The original raw ticket text and classification fields remain preserved from the source dataset.

## Output Database

The DuckDB database is created locally at:

`data/gold/customer_support_analytics.duckdb`

This database is not pushed to GitHub because data folders are ignored. The SQL and Python scripts are pushed instead so the database can be recreated.