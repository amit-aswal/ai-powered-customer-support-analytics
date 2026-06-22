# Phase 2 Feature Engineering Report

## Overview

Phase 2 converts the raw bronze support ticket dataset into a cleaned and business-ready silver dataset.

## Total Records

| Metric | Value |
|---|---:|
| Total Tickets | 61,765 |
| Total Columns After Feature Engineering | 41 |
| Closed Tickets | 43,245 |
| Open Tickets | 9,335 |
| Pending Tickets | 6,227 |
| Escalated Tickets | 2,958 |
| Average Resolution Time Hours | 48.27 |
| SLA Met Count | 32,690 |
| SLA Breached Count | 10,555 |

## Fields Created

- ticket_id
- subject_clean
- body_clean
- answer_clean
- combined_text
- combined_text_length
- type_clean
- queue_clean
- priority_clean
- language_clean
- version_clean
- status
- created_date
- resolved_date
- resolution_time_hours
- agent_name
- sla_target_hours
- sla_status
- tags_combined
- tag_count
- ticket_category_rule_based
- has_subject
- has_body
- has_answer
- is_operational_data_simulated

## Important Note

The original dataset does not contain operational support fields such as ticket status, created date, resolved date, resolution time, agent assignment, and SLA status.

These fields were engineered using reproducible business simulation logic to create a realistic enterprise customer support analytics environment.

## Business Value

The silver dataset is now ready for:

- SQL data modeling
- KPI calculation
- SLA analysis
- Queue workload analysis
- Agent performance analysis
- Ticket category analysis
- Power BI dashboards
- Streamlit application
- Future NLP and AI analysis