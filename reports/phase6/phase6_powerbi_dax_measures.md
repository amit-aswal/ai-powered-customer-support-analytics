# Phase 6 Power BI DAX Measures

Use these measures after loading `powerbi_fact_support_tickets_dashboard.csv` into Power BI.

Assumed table name:

`powerbi_fact_support_tickets_dashboard`

---

## Core KPI Measures

Total Tickets =
COUNTROWS(powerbi_fact_support_tickets_dashboard)

Open Tickets =
SUM(powerbi_fact_support_tickets_dashboard[is_open])

Closed Tickets =
SUM(powerbi_fact_support_tickets_dashboard[is_closed])

Pending Tickets =
SUM(powerbi_fact_support_tickets_dashboard[is_pending])

Escalated Tickets =
SUM(powerbi_fact_support_tickets_dashboard[is_escalated])

SLA Met Tickets =
SUM(powerbi_fact_support_tickets_dashboard[is_sla_met])

SLA Breached Tickets =
SUM(powerbi_fact_support_tickets_dashboard[is_sla_breached])

Average Resolution Time =
AVERAGE(powerbi_fact_support_tickets_dashboard[resolution_time_hours])

---

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

Escalated Ticket % =
DIVIDE(
    [Escalated Tickets],
    [Total Tickets],
    0
)
