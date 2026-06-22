from pathlib import Path
import duckdb
import pandas as pd


GOLD_DB = Path("data/gold/customer_support_analytics.duckdb")

POWERBI_EXPORT_DIR = Path("data/gold/powerbi_exports")
REPORT_DIR = Path("reports/phase5")
DASHBOARD_DATA_DIR = REPORT_DIR / "dashboard_data"

POWERBI_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_powerbi_export(df: pd.DataFrame, filename: str, save_to_reports: bool = True) -> None:
    powerbi_path = POWERBI_EXPORT_DIR / filename
    df.to_csv(powerbi_path, index=False, encoding="utf-8")
    print(f"Saved Power BI export: {powerbi_path}")

    if save_to_reports:
        report_path = DASHBOARD_DATA_DIR / filename
        df.to_csv(report_path, index=False, encoding="utf-8")
        print(f"Saved dashboard report data: {report_path}")


def create_dashboard_fact_table(con):
    query = """
        SELECT
            f.ticket_id,

            CAST(f.created_date AS DATE) AS created_date,
            CAST(f.resolved_date AS DATE) AS resolved_date,

            dd.year AS created_year,
            dd.quarter AS created_quarter,
            dd.month_number AS created_month_number,
            dd.month_name AS created_month_name,
            dd.day_name AS created_day_name,
            dd.is_weekend AS created_on_weekend,

            dq.queue_clean AS queue,
            dp.priority_clean AS priority,
            dl.language_clean AS language,
            da.agent_name,
            dcat.ticket_category,
            ds.status,
            dt.type_clean AS ticket_type,

            f.resolution_time_hours,
            f.sla_target_hours,
            f.combined_text_length,
            f.tag_count,

            f.is_closed,
            f.is_open,
            f.is_pending,
            f.is_escalated,
            f.is_sla_met,
            f.is_sla_breached,

            CASE
                WHEN f.is_sla_met = 1 THEN 'SLA Met'
                WHEN f.is_sla_breached = 1 THEN 'SLA Breached'
                ELSE 'Open / Not Applicable'
            END AS sla_status,

            f.has_subject,
            f.has_body,
            f.has_answer,
            f.is_operational_data_simulated

        FROM fact_support_tickets f

        LEFT JOIN dim_date dd
            ON f.created_date_key = dd.date_key

        LEFT JOIN dim_queue dq
            ON f.queue_key = dq.queue_key

        LEFT JOIN dim_priority dp
            ON f.priority_key = dp.priority_key

        LEFT JOIN dim_language dl
            ON f.language_key = dl.language_key

        LEFT JOIN dim_agent da
            ON f.agent_key = da.agent_key

        LEFT JOIN dim_ticket_category dcat
            ON f.category_key = dcat.category_key

        LEFT JOIN dim_status ds
            ON f.status_key = ds.status_key

        LEFT JOIN dim_type dt
            ON f.type_key = dt.type_key;
    """

    df = con.execute(query).df()

    # This is the main dashboard dataset. It is saved locally only because it contains all ticket rows.
    save_powerbi_export(df, "powerbi_fact_support_tickets_dashboard.csv", save_to_reports=False)


def create_kpi_summary(con):
    query = """
        SELECT
            COUNT(*) AS total_tickets,
            SUM(is_open) AS open_tickets,
            SUM(is_closed) AS closed_tickets,
            SUM(is_pending) AS pending_tickets,
            SUM(is_escalated) AS escalated_tickets,
            ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(is_sla_met) AS sla_met_tickets,
            SUM(is_sla_breached) AS sla_breached_tickets,
            ROUND(
                SUM(is_sla_met) * 100.0 /
                NULLIF(SUM(is_sla_met) + SUM(is_sla_breached), 0),
                2
            ) AS sla_compliance_percentage,
            ROUND(
                SUM(is_sla_breached) * 100.0 /
                NULLIF(SUM(is_sla_met) + SUM(is_sla_breached), 0),
                2
            ) AS sla_breach_percentage
        FROM fact_support_tickets;
    """

    df = con.execute(query).df()
    save_powerbi_export(df, "powerbi_kpi_summary.csv")


def create_status_summary(con):
    query = """
        SELECT
            ds.status,
            COUNT(*) AS ticket_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
        FROM fact_support_tickets f
        LEFT JOIN dim_status ds
            ON f.status_key = ds.status_key
        GROUP BY ds.status
        ORDER BY ticket_count DESC;
    """

    df = con.execute(query).df()
    save_powerbi_export(df, "powerbi_status_summary.csv")


def create_queue_summary(con):
    query = """
        SELECT
            dq.queue_clean AS queue,
            COUNT(*) AS total_tickets,
            SUM(f.is_closed) AS closed_tickets,
            SUM(f.is_open) AS open_tickets,
            SUM(f.is_pending) AS pending_tickets,
            SUM(f.is_escalated) AS escalated_tickets,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(f.is_sla_met) AS sla_met_tickets,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            ROUND(
                SUM(f.is_sla_met) * 100.0 /
                NULLIF(SUM(f.is_sla_met) + SUM(f.is_sla_breached), 0),
                2
            ) AS sla_compliance_percentage,
            RANK() OVER (ORDER BY COUNT(*) DESC) AS workload_rank
        FROM fact_support_tickets f
        LEFT JOIN dim_queue dq
            ON f.queue_key = dq.queue_key
        GROUP BY dq.queue_clean
        ORDER BY total_tickets DESC;
    """

    df = con.execute(query).df()
    save_powerbi_export(df, "powerbi_queue_summary.csv")


def create_priority_summary(con):
    query = """
        SELECT
            dp.priority_clean AS priority,
            COUNT(*) AS total_tickets,
            SUM(f.is_sla_met) AS sla_met_tickets,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            ROUND(
                SUM(f.is_sla_met) * 100.0 /
                NULLIF(SUM(f.is_sla_met) + SUM(f.is_sla_breached), 0),
                2
            ) AS sla_compliance_percentage,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours
        FROM fact_support_tickets f
        LEFT JOIN dim_priority dp
            ON f.priority_key = dp.priority_key
        GROUP BY dp.priority_clean
        ORDER BY sla_breached_tickets DESC;
    """

    df = con.execute(query).df()
    save_powerbi_export(df, "powerbi_priority_summary.csv")


def create_agent_summary(con):
    query = """
        SELECT
            da.agent_name,
            COUNT(*) AS assigned_tickets,
            SUM(f.is_closed) AS closed_tickets,
            SUM(f.is_open) AS open_tickets,
            SUM(f.is_pending) AS pending_tickets,
            SUM(f.is_escalated) AS escalated_tickets,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(f.is_sla_met) AS sla_met_tickets,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            RANK() OVER (ORDER BY COUNT(*) DESC) AS workload_rank
        FROM fact_support_tickets f
        LEFT JOIN dim_agent da
            ON f.agent_key = da.agent_key
        GROUP BY da.agent_name
        ORDER BY assigned_tickets DESC;
    """

    df = con.execute(query).df()
    save_powerbi_export(df, "powerbi_agent_summary.csv")


def create_category_summary(con):
    query = """
        SELECT
            dcat.ticket_category,
            COUNT(*) AS total_tickets,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(f.is_sla_met) AS sla_met_tickets,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            RANK() OVER (ORDER BY COUNT(*) DESC) AS category_rank
        FROM fact_support_tickets f
        LEFT JOIN dim_ticket_category dcat
            ON f.category_key = dcat.category_key
        GROUP BY dcat.ticket_category
        ORDER BY total_tickets DESC;
    """

    df = con.execute(query).df()
    save_powerbi_export(df, "powerbi_category_summary.csv")


def create_monthly_summary(con):
    query = """
        SELECT
            dd.year,
            dd.month_number,
            dd.month_name,
            dd.year || '-' || LPAD(CAST(dd.month_number AS VARCHAR), 2, '0') AS year_month,
            COUNT(*) AS total_tickets,
            SUM(f.is_closed) AS closed_tickets,
            SUM(f.is_open) AS open_tickets,
            SUM(f.is_sla_met) AS sla_met_tickets,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours
        FROM fact_support_tickets f
        LEFT JOIN dim_date dd
            ON f.created_date_key = dd.date_key
        GROUP BY dd.year, dd.month_number, dd.month_name
        ORDER BY dd.year, dd.month_number;
    """

    df = con.execute(query).df()
    save_powerbi_export(df, "powerbi_monthly_summary.csv")


def create_sla_breach_driver_summary(con):
    query = """
        SELECT
            dq.queue_clean AS queue,
            dcat.ticket_category,
            dp.priority_clean AS priority,
            COUNT(*) AS breached_tickets
        FROM fact_support_tickets f
        LEFT JOIN dim_queue dq
            ON f.queue_key = dq.queue_key
        LEFT JOIN dim_ticket_category dcat
            ON f.category_key = dcat.category_key
        LEFT JOIN dim_priority dp
            ON f.priority_key = dp.priority_key
        WHERE f.is_sla_breached = 1
        GROUP BY dq.queue_clean, dcat.ticket_category, dp.priority_clean
        ORDER BY breached_tickets DESC
        LIMIT 20;
    """

    df = con.execute(query).df()
    save_powerbi_export(df, "powerbi_top_sla_breach_drivers.csv")


def create_powerbi_measure_reference():
    measure_text = """
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
"""

    output_path = REPORT_DIR / "phase5_powerbi_measure_reference.md"
    output_path.write_text(measure_text.strip(), encoding="utf-8")
    print(f"Saved: {output_path}")


def create_dashboard_plan():
    dashboard_plan = """
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
"""

    output_path = REPORT_DIR / "phase5_powerbi_dashboard_plan.md"
    output_path.write_text(dashboard_plan.strip(), encoding="utf-8")
    print(f"Saved: {output_path}")


def create_phase5_summary_report():
    summary = """
# Phase 5 Dashboard Dataset Preparation Report

## Objective

Phase 5 prepares the customer support analytics project for Power BI dashboard development.

This phase creates dashboard-ready CSV files, KPI summary tables, Power BI measure references, and dashboard planning documentation.

## Main Output Folder

Power BI local export files:

`data/gold/powerbi_exports/`

GitHub report preview files:

`reports/phase5/dashboard_data/`

## Files Created

### Main Dashboard Dataset

- powerbi_fact_support_tickets_dashboard.csv

### Summary Tables

- powerbi_kpi_summary.csv
- powerbi_status_summary.csv
- powerbi_queue_summary.csv
- powerbi_priority_summary.csv
- powerbi_agent_summary.csv
- powerbi_category_summary.csv
- powerbi_monthly_summary.csv
- powerbi_top_sla_breach_drivers.csv

### Documentation

- phase5_powerbi_dashboard_plan.md
- phase5_powerbi_measure_reference.md
- phase5_dashboard_dataset_preparation_report.md

## Business Value

The Phase 5 outputs make it easy to build a Power BI dashboard for:

- Executive KPI monitoring
- Queue workload analysis
- SLA compliance tracking
- Agent workload comparison
- Ticket category analysis
- Monthly support trend analysis

## Next Step

The next step is to open Power BI Desktop and import the files from:

`data/gold/powerbi_exports/`

Then create visuals based on the dashboard plan.
"""

    output_path = REPORT_DIR / "phase5_dashboard_dataset_preparation_report.md"
    output_path.write_text(summary.strip(), encoding="utf-8")
    print(f"Saved: {output_path}")


def main():
    if not GOLD_DB.exists():
        raise FileNotFoundError(
            "Gold DuckDB database not found. Complete Phase 3 before running Phase 5."
        )

    con = duckdb.connect(str(GOLD_DB))

    print("Creating Power BI dashboard fact table...")
    create_dashboard_fact_table(con)

    print("Creating KPI summary...")
    create_kpi_summary(con)

    print("Creating status summary...")
    create_status_summary(con)

    print("Creating queue summary...")
    create_queue_summary(con)

    print("Creating priority summary...")
    create_priority_summary(con)

    print("Creating agent summary...")
    create_agent_summary(con)

    print("Creating category summary...")
    create_category_summary(con)

    print("Creating monthly summary...")
    create_monthly_summary(con)

    print("Creating SLA breach driver summary...")
    create_sla_breach_driver_summary(con)

    con.close()

    print("Creating Power BI measure reference...")
    create_powerbi_measure_reference()

    print("Creating dashboard plan...")
    create_dashboard_plan()

    print("Creating Phase 5 summary report...")
    create_phase5_summary_report()

    print("Phase 5 Power BI dataset preparation completed successfully.")


if __name__ == "__main__":
    main()
