# Phase 1 Data Profile Report

## Dataset Overview

| Metric | Value |
|---|---:|
| Total Rows | 61,765 |
| Total Columns | 16 |
| Possible Duplicate Tickets | 8,306 |

## Raw Columns

subject, body, answer, type, queue, priority, language, version, tag_1, tag_2, tag_3, tag_4, tag_5, tag_6, tag_7, tag_8

## Top Missing Value Columns

| column_name   |   missing_count |   missing_percentage |
|:--------------|----------------:|---------------------:|
| tag_8         |           59293 |                96    |
| tag_7         |           55797 |                90.34 |
| tag_6         |           48540 |                78.59 |
| tag_5         |           34129 |                55.26 |
| version       |           33178 |                53.72 |
| tag_4         |           17775 |                28.78 |
| tag_3         |           13409 |                21.71 |
| tag_2         |           13237 |                21.43 |
| answer        |           13189 |                21.35 |
| type          |           13178 |                21.34 |

## Missing Business Fields

| field_name            | exists_in_raw_dataset   | action_needed                | business_use                                          |
|:----------------------|:------------------------|:-----------------------------|:------------------------------------------------------|
| ticket_id             | False                   | Engineer in Phase 2 or later | Unique ticket identifier for fact table and tracking  |
| status                | False                   | Engineer in Phase 2 or later | Open, closed, pending, and escalated ticket reporting |
| created_date          | False                   | Engineer in Phase 2 or later | Daily, weekly, and monthly ticket trend analysis      |
| resolved_date         | False                   | Engineer in Phase 2 or later | Resolution performance tracking                       |
| resolution_time_hours | False                   | Engineer in Phase 2 or later | Average resolution time KPI                           |
| agent_name            | False                   | Engineer in Phase 2 or later | Agent workload and performance analysis               |
| sla_status            | False                   | Engineer in Phase 2 or later | SLA compliance reporting                              |
| sentiment             | False                   | Engineer in Phase 2 or later | Customer experience and complaint sentiment tracking  |
| ticket_category       | False                   | Engineer in Phase 2 or later | Root cause and complaint driver analysis              |

## Initial Business Understanding

The raw dataset contains customer support ticket text, ticket type, queue, priority, language, version, and tag fields.

These fields are useful for:

- Ticket volume analysis
- Queue workload analysis
- Priority distribution analysis
- Language-based support analysis
- NLP-based ticket classification
- AI-generated summaries
- Root cause analysis

However, the dataset does not contain several operational fields required for enterprise support analytics.

Missing operational fields include:

- ticket_id
- status
- created_date
- resolved_date
- resolution_time_hours
- agent_name
- sla_status
- sentiment
- ticket_category

These fields will be created in the silver layer using documented feature engineering logic.

## Business Risk

If operational fields are not engineered properly, dashboards will not be able to answer important leadership questions such as:

- How many tickets are open?
- How many tickets are closed?
- What is the average resolution time?
- Which teams are overloaded?
- Which tickets breached SLA?
- What are the biggest complaint drivers?

## Next Phase

Phase 2 will clean the raw data and create engineered business fields such as ticket_id, status, created_date, resolved_date, resolution_time_hours, agent_name, and sla_status.