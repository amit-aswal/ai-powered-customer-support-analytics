# Phase 4 EDA and Business Insights Report

## Objective

Phase 4 analyzes the SQL analytics model created in Phase 3 and converts KPI outputs into business insights.

This phase focuses on understanding ticket volume, workload pressure, SLA performance, issue categories, monthly trends, agent workload, and operational risks.

---

## Executive Summary

The support dataset contains **61,765 tickets**.

Out of these:

| Metric | Value |
|---|---:|
| Total Tickets | 61,765 |
| Closed Tickets | 43,245 |
| Open Tickets | 9,335 |
| Pending Tickets | 6,227 |
| Escalated Tickets | 2,958 |
| Average Resolution Time Hours | 48.27 |
| SLA Met Tickets | 32,690 |
| SLA Breached Tickets | 10,555 |
| SLA Compliance Percentage | 75.59% |

---

## Key Business Insights

### 1. Ticket Workload Is Concentrated in Specific Queues

The highest workload queue is **technical support** with **14,186 tickets**.

This means support leadership should monitor this queue closely because high volume may lead to slower response time, agent overload, and higher SLA breach risk.

### 2. Top Complaint Category

The largest ticket category is **Other** with **34,928 tickets**, representing **56.55%** of all tickets.

This category should be reviewed for root-cause analysis because reducing this issue can reduce total support volume.

### 3. SLA Breach Risk Exists

The dataset has **10,555 SLA breached tickets**.

The priority group with the highest SLA breach count is **medium** with **4,412 breached tickets**.

This indicates that priority handling rules and escalation workflows should be reviewed.

### 4. Agent Workload Is Uneven

The agent with the highest assigned workload is **Pooja Menon** with **8,575 assigned tickets**.

This may indicate workload imbalance. Management can use this insight to rebalance ticket assignments.

### 5. Monthly Ticket Volume Trend

The month with the highest ticket volume is **2024-03** with **3,567 tickets**.

This helps support leaders identify peak workload periods and plan staffing accordingly.


### 6. Month-over-Month Growth

The highest month-over-month growth occurred in **2024-03**, with a growth rate of **9.82%**.

This type of increase should be investigated because sudden ticket growth can indicate product issues, billing issues, outages, process failures, or customer communication gaps.


### 7. Top SLA Breach Driver

The top SLA breach driver is:

| Queue | Category | Priority | Breached Tickets |
|---|---|---|---:|
| technical support | Technical Issues | high | 563 |

This combination should be prioritized for operational improvement.


### 8. Text Data Is Useful for NLP

The average combined ticket text length is **463.42 characters**.

This confirms that the dataset has enough text content to support future NLP tasks such as sentiment analysis, topic modeling, root cause analysis, and AI-generated summaries.

---

## Business Recommendations

### Recommendation 1: Monitor High-Volume Queues

The highest-volume queues should be monitored weekly. If volume remains high, the business should consider adding more agents, improving self-service documentation, or automating repeated responses.

### Recommendation 2: Investigate Top Ticket Categories

The most common categories should be reviewed with product, operations, and customer success teams. Reducing one high-volume category can reduce support workload significantly.

### Recommendation 3: Reduce SLA Breaches

SLA breach drivers should be reviewed by queue, priority, and category. High-breach areas may need faster escalation, better routing, or more trained agents.

### Recommendation 4: Balance Agent Workload

Agents with unusually high assigned ticket counts should be reviewed. Workload balancing can improve response time and reduce burnout.

### Recommendation 5: Use Monthly Trends for Staffing

Monthly ticket trends can help support managers plan staffing, training, and automation before high-volume periods.

---

## Important Note

Some operational fields such as status, created_date, resolved_date, resolution_time_hours, agent_name, and SLA status were simulated in Phase 2 because the original dataset does not include real ticket lifecycle fields.

The analysis is designed to demonstrate how a real customer support analytics workflow would operate.

---

## Phase 4 Outputs

### CSV Reports

- phase4_executive_kpi.csv
- phase4_status_distribution.csv
- phase4_queue_performance.csv
- phase4_priority_sla.csv
- phase4_agent_performance.csv
- phase4_category_analysis.csv
- phase4_monthly_trend.csv
- phase4_mom_growth.csv
- phase4_top_sla_breach_drivers.csv
- phase4_text_quality.csv

### Charts

- ticket_volume_by_status.png
- top_10_queues_by_volume.png
- ticket_volume_by_category.png
- monthly_ticket_volume_trend.png
- sla_breaches_by_priority.png
- top_10_agents_by_workload.png

---

## Next Step

The next phase can use these insights to design a Power BI dashboard with executive, operations, SLA, category, and trend pages.