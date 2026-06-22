# Phase 5 Power BI Measure Reference

Use these DAX measures in Power BI after loading the dashboard CSV files.

## Core Measures

Total Tickets = COUNTROWS(powerbi_fact_support_tickets_dashboard)

Open Tickets = SUM(powerbi_fact_support_tickets_dashboard[is_open])

Closed Tickets = SUM(powerbi_fact_support_tickets_dashboard[is_closed])

Pending Tickets = SUM(powerbi_fact_support_tickets_dashboard[is_pending])

Escalated Tickets = SUM(powerbi_fact_support_tickets_dashboard[is_escalated])

SLA Met Tickets = SUM(powerbi_fact_support_tickets_dashboard[is_sla_met])

SLA Breached Tickets = SUM(powerbi_fact_support_tickets_dashboard[is_sla_breached])

Average Resolution Time = AVERAGE(powerbi_fact_support_tickets_dashboard[resolution_time_hours])

## Percentage Measures

SLA Compliance % =
DIVIDE(
    [SLA Met Tickets],
    [SLA Met Tickets] + [SLA Breached Tickets],
    0
)

SLA Breach % =
DIVIDE(
    [SLA Breached Tickets],
    [SLA Met Tickets] + [SLA Breached Tickets],
    0
)

Open Ticket % =
DIVIDE(
    [Open Tickets],
    [Total Tickets],
    0
)

Closed Ticket % =
DIVIDE(
    [Closed Tickets],
    [Total Tickets],
    0
)

## Dashboard Usage

Use these measures for KPI cards, bar charts, trend charts, and SLA performance visuals.