# Phase 6 Power BI Dashboard Build Guide

## Objective

Phase 6 builds a Power BI dashboard for the AI-Powered Customer Support Analytics Platform.

The dashboard converts cleaned and modeled customer support ticket data into business visuals for leadership and operations teams.

---

## Dataset to Import

Import this file into Power BI Desktop:

`data/gold/powerbi_exports/powerbi_fact_support_tickets_dashboard.csv`

---

## Dashboard Pages

The Power BI dashboard will contain these pages:

1. Executive Overview
2. Queue Performance
3. SLA Performance
4. Agent Workload
5. Ticket Category Analysis
6. Monthly Trend Analysis

---

## Page 1: Executive Overview

### KPI Cards

- Total Tickets
- Open Tickets
- Closed Tickets
- Pending Tickets
- Escalated Tickets
- Average Resolution Time
- SLA Compliance %
- SLA Breached Tickets

### Charts

- Ticket Volume by Status
- Monthly Ticket Volume Trend
- Ticket Category Distribution
- Top Queues by Ticket Volume

---

## Page 2: Queue Performance

### Charts

- Tickets by Queue
- SLA Breached Tickets by Queue
- Average Resolution Time by Queue
- Open Tickets by Queue

---

## Page 3: SLA Performance

### Charts

- SLA Met vs SLA Breached
- SLA Breach by Priority
- SLA Breach by Queue
- SLA Compliance by Priority

---

## Page 4: Agent Workload

### Charts

- Assigned Tickets by Agent
- Closed Tickets by Agent
- Open Tickets by Agent
- SLA Breached Tickets by Agent

---

## Page 5: Ticket Category Analysis

### Charts

- Tickets by Category
- Average Resolution Time by Category
- SLA Breaches by Category
- Category by Priority

---

## Page 6: Monthly Trend Analysis

### Charts

- Monthly Ticket Volume
- Monthly Open Tickets
- Monthly SLA Breaches
- Average Resolution Time Trend

---

## Recommended Slicers

- created_year
- created_month_name
- queue
- priority
- status
- agent_name
- ticket_category
- language
- sla_status

---

## Save Power BI File

Save the dashboard as:

`dashboards/powerbi/customer_support_analytics_dashboard.pbix`

---

## Screenshots for GitHub

Save dashboard screenshots in:

`reports/phase6/screenshots/`

Recommended screenshots:

- executive_overview.png
- queue_performance.png
- sla_performance.png
- agent_workload.png
- ticket_category_analysis.png
- monthly_trend_analysis.png

---

## Important Note

Some operational fields used in this dashboard were simulated in Phase 2 because the original dataset does not include real ticket lifecycle fields.
