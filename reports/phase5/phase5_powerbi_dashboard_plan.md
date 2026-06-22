# Phase 5 Power BI Dashboard Plan

## Objective

The objective of Phase 5 is to prepare dashboard-ready datasets and design a Power BI dashboard plan for the AI-Powered Customer Support Analytics Platform.

The dashboard will help support leaders monitor ticket volume, SLA performance, queue workload, agent workload, ticket categories, and monthly support trends.

---

## Dashboard Page 1: Executive Overview

### Purpose

Give leadership a quick overview of customer support performance.

### KPI Cards

- Total Tickets
- Open Tickets
- Closed Tickets
- Pending Tickets
- Escalated Tickets
- Average Resolution Time
- SLA Compliance %
- SLA Breached Tickets

### Visuals

- Ticket Volume by Status
- Monthly Ticket Volume Trend
- Ticket Category Distribution
- Top Queues by Ticket Volume

### Business Question Answered

- How many tickets are being handled?
- What is the current support workload?
- Is SLA performance healthy?
- Which areas need attention?

---

## Dashboard Page 2: Queue Performance

### Purpose

Analyze workload and performance across support queues.

### Visuals

- Tickets by Queue
- SLA Breached Tickets by Queue
- Average Resolution Time by Queue
- Open Tickets by Queue

### Business Question Answered

- Which support teams are overloaded?
- Which queues have slow resolution?
- Which queues have more SLA breaches?

---

## Dashboard Page 3: SLA Performance

### Purpose

Monitor SLA compliance and breach risk.

### Visuals

- SLA Met vs SLA Breached
- SLA Breach by Priority
- SLA Breach by Queue
- Top SLA Breach Drivers

### Business Question Answered

- Are tickets being resolved within SLA?
- Which priority levels breach SLA most?
- Which queue-category-priority combinations need action?

---

## Dashboard Page 4: Agent Workload

### Purpose

Compare ticket workload across support agents.

### Visuals

- Assigned Tickets by Agent
- Closed Tickets by Agent
- Open Tickets by Agent
- SLA Breached Tickets by Agent
- Average Resolution Time by Agent

### Business Question Answered

- Which agents have the highest workload?
- Is workload balanced?
- Which agents need support or training?

---

## Dashboard Page 5: Ticket Category Analysis

### Purpose

Identify the most common customer issue categories.

### Visuals

- Tickets by Category
- Category Share %
- Average Resolution Time by Category
- SLA Breaches by Category

### Business Question Answered

- What are customers complaining about most?
- Which issue categories create the highest support demand?
- Which categories need root-cause analysis?

---

## Dashboard Page 6: Monthly Trend Analysis

### Purpose

Analyze support demand over time.

### Visuals

- Monthly Ticket Volume
- Monthly Open Tickets
- Monthly Closed Tickets
- Monthly SLA Breaches
- Average Resolution Time Trend

### Business Question Answered

- Is ticket volume increasing or decreasing?
- Which months have high support pressure?
- Are SLA breaches increasing over time?

---

## Recommended Slicers

Use these filters across dashboard pages:

- Created Year
- Created Month
- Queue
- Priority
- Status
- Agent Name
- Ticket Category
- Language
- SLA Status

---

## Power BI Dataset Files

The dashboard-ready files are created locally in:

`data/gold/powerbi_exports/`

Important files:

- powerbi_fact_support_tickets_dashboard.csv
- powerbi_kpi_summary.csv
- powerbi_status_summary.csv
- powerbi_queue_summary.csv
- powerbi_priority_summary.csv
- powerbi_agent_summary.csv
- powerbi_category_summary.csv
- powerbi_monthly_summary.csv
- powerbi_top_sla_breach_drivers.csv

---

## Important Note

The operational fields used in this dashboard, such as ticket status, created date, resolved date, agent name, resolution time, and SLA status, were simulated in Phase 2 because the original dataset does not include real lifecycle fields.

This is clearly documented to keep the project transparent.