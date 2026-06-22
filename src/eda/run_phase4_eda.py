from pathlib import Path
import duckdb
import pandas as pd
import matplotlib.pyplot as plt


GOLD_DB = Path("data/gold/customer_support_analytics.duckdb")
REPORT_DIR = Path("reports/phase4")
CHART_DIR = REPORT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


def save_dataframe(df: pd.DataFrame, filename: str) -> None:
    output_path = REPORT_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Saved: {output_path}")


def save_bar_chart(df, x_col, y_col, title, xlabel, ylabel, filename, horizontal=False):
    plt.figure(figsize=(10, 6))

    if horizontal:
        plt.barh(df[y_col], df[x_col])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.gca().invert_yaxis()
    else:
        plt.bar(df[x_col], df[y_col])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha="right")

    plt.title(title)
    plt.tight_layout()

    output_path = CHART_DIR / filename
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Saved chart: {output_path}")


def save_line_chart(df, x_col, y_col, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = CHART_DIR / filename
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Saved chart: {output_path}")


def get_dataframes(con):
    executive_kpi = con.execute("""
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
            ) AS sla_compliance_percentage
        FROM fact_support_tickets;
    """).df()

    status_distribution = con.execute("""
        SELECT
            ds.status,
            COUNT(*) AS ticket_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
        FROM fact_support_tickets f
        LEFT JOIN dim_status ds
            ON f.status_key = ds.status_key
        GROUP BY ds.status
        ORDER BY ticket_count DESC;
    """).df()

    queue_performance = con.execute("""
        SELECT
            dq.queue_clean,
            COUNT(*) AS total_tickets,
            SUM(f.is_closed) AS closed_tickets,
            SUM(f.is_open) AS open_tickets,
            SUM(f.is_pending) AS pending_tickets,
            SUM(f.is_escalated) AS escalated_tickets,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            RANK() OVER (ORDER BY COUNT(*) DESC) AS workload_rank
        FROM fact_support_tickets f
        LEFT JOIN dim_queue dq
            ON f.queue_key = dq.queue_key
        GROUP BY dq.queue_clean
        ORDER BY total_tickets DESC;
    """).df()

    priority_sla = con.execute("""
        SELECT
            dp.priority_clean,
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
    """).df()

    agent_performance = con.execute("""
        SELECT
            da.agent_name,
            COUNT(*) AS assigned_tickets,
            SUM(f.is_closed) AS closed_tickets,
            SUM(f.is_open) AS open_tickets,
            SUM(f.is_escalated) AS escalated_tickets,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            RANK() OVER (ORDER BY COUNT(*) DESC) AS workload_rank
        FROM fact_support_tickets f
        LEFT JOIN dim_agent da
            ON f.agent_key = da.agent_key
        GROUP BY da.agent_name
        ORDER BY assigned_tickets DESC;
    """).df()

    category_analysis = con.execute("""
        SELECT
            dcat.ticket_category,
            COUNT(*) AS total_tickets,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            RANK() OVER (ORDER BY COUNT(*) DESC) AS category_rank
        FROM fact_support_tickets f
        LEFT JOIN dim_ticket_category dcat
            ON f.category_key = dcat.category_key
        GROUP BY dcat.ticket_category
        ORDER BY total_tickets DESC;
    """).df()

    monthly_trend = con.execute("""
        SELECT
            dd.year,
            dd.month_number,
            dd.month_name,
            dd.year || '-' || LPAD(CAST(dd.month_number AS VARCHAR), 2, '0') AS year_month,
            COUNT(*) AS total_tickets,
            SUM(f.is_closed) AS closed_tickets,
            SUM(f.is_open) AS open_tickets,
            SUM(f.is_sla_breached) AS sla_breached_tickets,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours
        FROM fact_support_tickets f
        LEFT JOIN dim_date dd
            ON f.created_date_key = dd.date_key
        GROUP BY dd.year, dd.month_number, dd.month_name
        ORDER BY dd.year, dd.month_number;
    """).df()

    mom_growth = con.execute("""
        WITH monthly_tickets AS (
            SELECT
                dd.year,
                dd.month_number,
                dd.month_name,
                dd.year || '-' || LPAD(CAST(dd.month_number AS VARCHAR), 2, '0') AS year_month,
                COUNT(*) AS total_tickets
            FROM fact_support_tickets f
            LEFT JOIN dim_date dd
                ON f.created_date_key = dd.date_key
            GROUP BY dd.year, dd.month_number, dd.month_name
        ),

        monthly_growth AS (
            SELECT
                year,
                month_number,
                month_name,
                year_month,
                total_tickets,
                LAG(total_tickets) OVER (
                    ORDER BY year, month_number
                ) AS previous_month_tickets
            FROM monthly_tickets
        )

        SELECT
            year,
            month_number,
            month_name,
            year_month,
            total_tickets,
            previous_month_tickets,
            total_tickets - previous_month_tickets AS ticket_change,
            ROUND(
                (total_tickets - previous_month_tickets) * 100.0 /
                NULLIF(previous_month_tickets, 0),
                2
            ) AS mom_growth_percentage
        FROM monthly_growth
        ORDER BY year, month_number;
    """).df()

    top_sla_breach_drivers = con.execute("""
        SELECT
            dq.queue_clean,
            dcat.ticket_category,
            dp.priority_clean,
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
    """).df()

    text_quality = con.execute("""
        SELECT
            COUNT(*) AS total_tickets,
            SUM(CASE WHEN has_subject = TRUE THEN 1 ELSE 0 END) AS tickets_with_subject,
            SUM(CASE WHEN has_body = TRUE THEN 1 ELSE 0 END) AS tickets_with_body,
            SUM(CASE WHEN has_answer = TRUE THEN 1 ELSE 0 END) AS tickets_with_answer,
            ROUND(AVG(combined_text_length), 2) AS avg_combined_text_length,
            MIN(combined_text_length) AS min_combined_text_length,
            MAX(combined_text_length) AS max_combined_text_length
        FROM fact_support_tickets;
    """).df()

    return {
        "executive_kpi": executive_kpi,
        "status_distribution": status_distribution,
        "queue_performance": queue_performance,
        "priority_sla": priority_sla,
        "agent_performance": agent_performance,
        "category_analysis": category_analysis,
        "monthly_trend": monthly_trend,
        "mom_growth": mom_growth,
        "top_sla_breach_drivers": top_sla_breach_drivers,
        "text_quality": text_quality
    }


def save_all_csvs(dataframes):
    for name, df in dataframes.items():
        save_dataframe(df, f"phase4_{name}.csv")


def create_charts(dataframes):
    status_distribution = dataframes["status_distribution"]
    queue_performance = dataframes["queue_performance"].head(10)
    category_analysis = dataframes["category_analysis"]
    monthly_trend = dataframes["monthly_trend"]
    priority_sla = dataframes["priority_sla"]
    agent_performance = dataframes["agent_performance"].head(10)

    save_bar_chart(
        status_distribution,
        x_col="status",
        y_col="ticket_count",
        title="Ticket Volume by Status",
        xlabel="Status",
        ylabel="Ticket Count",
        filename="ticket_volume_by_status.png"
    )

    save_bar_chart(
        queue_performance.sort_values("total_tickets", ascending=True),
        x_col="total_tickets",
        y_col="queue_clean",
        title="Top 10 Queues by Ticket Volume",
        xlabel="Ticket Count",
        ylabel="Queue",
        filename="top_10_queues_by_volume.png",
        horizontal=True
    )

    save_bar_chart(
        category_analysis.sort_values("total_tickets", ascending=True),
        x_col="total_tickets",
        y_col="ticket_category",
        title="Ticket Volume by Category",
        xlabel="Ticket Count",
        ylabel="Ticket Category",
        filename="ticket_volume_by_category.png",
        horizontal=True
    )

    save_line_chart(
        monthly_trend,
        x_col="year_month",
        y_col="total_tickets",
        title="Monthly Ticket Volume Trend",
        xlabel="Month",
        ylabel="Ticket Count",
        filename="monthly_ticket_volume_trend.png"
    )

    save_bar_chart(
        priority_sla,
        x_col="priority_clean",
        y_col="sla_breached_tickets",
        title="SLA Breached Tickets by Priority",
        xlabel="Priority",
        ylabel="SLA Breached Tickets",
        filename="sla_breaches_by_priority.png"
    )

    save_bar_chart(
        agent_performance.sort_values("assigned_tickets", ascending=True),
        x_col="assigned_tickets",
        y_col="agent_name",
        title="Top 10 Agents by Assigned Tickets",
        xlabel="Assigned Tickets",
        ylabel="Agent",
        filename="top_10_agents_by_workload.png",
        horizontal=True
    )


def get_value(df, column):
    return df[column].iloc[0]


def create_business_insight_report(dataframes):
    executive = dataframes["executive_kpi"]
    queue = dataframes["queue_performance"]
    category = dataframes["category_analysis"]
    agent = dataframes["agent_performance"]
    priority = dataframes["priority_sla"]
    monthly = dataframes["monthly_trend"]
    mom = dataframes["mom_growth"]
    breach_drivers = dataframes["top_sla_breach_drivers"]
    text_quality = dataframes["text_quality"]

    total_tickets = int(get_value(executive, "total_tickets"))
    open_tickets = int(get_value(executive, "open_tickets"))
    closed_tickets = int(get_value(executive, "closed_tickets"))
    pending_tickets = int(get_value(executive, "pending_tickets"))
    escalated_tickets = int(get_value(executive, "escalated_tickets"))
    avg_resolution_time = get_value(executive, "avg_resolution_time_hours")
    sla_met = int(get_value(executive, "sla_met_tickets"))
    sla_breached = int(get_value(executive, "sla_breached_tickets"))
    sla_compliance = get_value(executive, "sla_compliance_percentage")

    top_queue = queue.iloc[0]
    top_category = category.iloc[0]
    top_agent = agent.iloc[0]
    top_priority_breach = priority.iloc[0]
    highest_month = monthly.sort_values("total_tickets", ascending=False).iloc[0]

    mom_non_null = mom.dropna(subset=["mom_growth_percentage"])
    if len(mom_non_null) > 0:
        highest_growth_month = mom_non_null.sort_values("mom_growth_percentage", ascending=False).iloc[0]
    else:
        highest_growth_month = None

    if len(breach_drivers) > 0:
        top_breach_driver = breach_drivers.iloc[0]
    else:
        top_breach_driver = None

    avg_text_length = get_value(text_quality, "avg_combined_text_length")

    report = f"""
# Phase 4 EDA and Business Insights Report

## Objective

Phase 4 analyzes the SQL analytics model created in Phase 3 and converts KPI outputs into business insights.

This phase focuses on understanding ticket volume, workload pressure, SLA performance, issue categories, monthly trends, agent workload, and operational risks.

---

## Executive Summary

The support dataset contains **{total_tickets:,} tickets**.

Out of these:

| Metric | Value |
|---|---:|
| Total Tickets | {total_tickets:,} |
| Closed Tickets | {closed_tickets:,} |
| Open Tickets | {open_tickets:,} |
| Pending Tickets | {pending_tickets:,} |
| Escalated Tickets | {escalated_tickets:,} |
| Average Resolution Time Hours | {avg_resolution_time} |
| SLA Met Tickets | {sla_met:,} |
| SLA Breached Tickets | {sla_breached:,} |
| SLA Compliance Percentage | {sla_compliance}% |

---

## Key Business Insights

### 1. Ticket Workload Is Concentrated in Specific Queues

The highest workload queue is **{top_queue["queue_clean"]}** with **{int(top_queue["total_tickets"]):,} tickets**.

This means support leadership should monitor this queue closely because high volume may lead to slower response time, agent overload, and higher SLA breach risk.

### 2. Top Complaint Category

The largest ticket category is **{top_category["ticket_category"]}** with **{int(top_category["total_tickets"]):,} tickets**, representing **{top_category["ticket_percentage"]}%** of all tickets.

This category should be reviewed for root-cause analysis because reducing this issue can reduce total support volume.

### 3. SLA Breach Risk Exists

The dataset has **{sla_breached:,} SLA breached tickets**.

The priority group with the highest SLA breach count is **{top_priority_breach["priority_clean"]}** with **{int(top_priority_breach["sla_breached_tickets"]):,} breached tickets**.

This indicates that priority handling rules and escalation workflows should be reviewed.

### 4. Agent Workload Is Uneven

The agent with the highest assigned workload is **{top_agent["agent_name"]}** with **{int(top_agent["assigned_tickets"]):,} assigned tickets**.

This may indicate workload imbalance. Management can use this insight to rebalance ticket assignments.

### 5. Monthly Ticket Volume Trend

The month with the highest ticket volume is **{highest_month["year_month"]}** with **{int(highest_month["total_tickets"]):,} tickets**.

This helps support leaders identify peak workload periods and plan staffing accordingly.
"""

    if highest_growth_month is not None:
        report += f"""

### 6. Month-over-Month Growth

The highest month-over-month growth occurred in **{highest_growth_month["year_month"]}**, with a growth rate of **{highest_growth_month["mom_growth_percentage"]}%**.

This type of increase should be investigated because sudden ticket growth can indicate product issues, billing issues, outages, process failures, or customer communication gaps.
"""

    if top_breach_driver is not None:
        report += f"""

### 7. Top SLA Breach Driver

The top SLA breach driver is:

| Queue | Category | Priority | Breached Tickets |
|---|---|---|---:|
| {top_breach_driver["queue_clean"]} | {top_breach_driver["ticket_category"]} | {top_breach_driver["priority_clean"]} | {int(top_breach_driver["breached_tickets"]):,} |

This combination should be prioritized for operational improvement.
"""

    report += f"""

### 8. Text Data Is Useful for NLP

The average combined ticket text length is **{avg_text_length} characters**.

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
"""

    output_path = REPORT_DIR / "phase4_eda_business_insights_report.md"
    output_path.write_text(report.strip(), encoding="utf-8")

    print(f"Saved insight report: {output_path}")


def main():
    if not GOLD_DB.exists():
        raise FileNotFoundError(
            "Gold DuckDB database not found. Complete Phase 3 before running Phase 4."
        )

    con = duckdb.connect(str(GOLD_DB))

    print("Running Phase 4 EDA queries...")
    dataframes = get_dataframes(con)

    print("Saving Phase 4 CSV outputs...")
    save_all_csvs(dataframes)

    print("Creating Phase 4 charts...")
    create_charts(dataframes)

    print("Creating Phase 4 business insight report...")
    create_business_insight_report(dataframes)

    con.close()

    print("Phase 4 EDA and business insights completed successfully.")


if __name__ == "__main__":
    main()
