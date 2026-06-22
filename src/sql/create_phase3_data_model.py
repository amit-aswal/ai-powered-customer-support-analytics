from pathlib import Path
import duckdb
import pandas as pd


SILVER_FILE = Path("data/silver/support_tickets_silver.parquet")
GOLD_DB = Path("data/gold/customer_support_analytics.duckdb")
REPORT_DIR = Path("reports/phase3")

REPORT_DIR.mkdir(parents=True, exist_ok=True)
GOLD_DB.parent.mkdir(parents=True, exist_ok=True)


def run_query_to_csv(con, query: str, output_file: str) -> None:
    df = con.execute(query).df()
    output_path = REPORT_DIR / output_file
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Saved report: {output_path}")


def create_star_schema(con):
    """
    Creates dimension and fact tables using the silver support ticket dataset.
    """

    con.execute(f"""
        CREATE OR REPLACE VIEW silver_support_tickets AS
        SELECT *
        FROM read_parquet('{SILVER_FILE.as_posix()}');
    """)

    print("Created view: silver_support_tickets")

    # Dimension: Date
    con.execute("""
        CREATE OR REPLACE TABLE dim_date AS
        WITH date_values AS (
            SELECT DISTINCT CAST(created_date AS DATE) AS date_value
            FROM silver_support_tickets
            WHERE created_date IS NOT NULL

            UNION

            SELECT DISTINCT CAST(resolved_date AS DATE) AS date_value
            FROM silver_support_tickets
            WHERE resolved_date IS NOT NULL
        )

        SELECT
            CAST(strftime(date_value, '%Y%m%d') AS INTEGER) AS date_key,
            date_value,
            EXTRACT(year FROM date_value) AS year,
            EXTRACT(quarter FROM date_value) AS quarter,
            EXTRACT(month FROM date_value) AS month_number,
            strftime(date_value, '%B') AS month_name,
            EXTRACT(day FROM date_value) AS day_of_month,
            EXTRACT(dayofweek FROM date_value) AS day_of_week_number,
            strftime(date_value, '%A') AS day_name,
            CASE
                WHEN EXTRACT(dayofweek FROM date_value) IN (0, 6)
                THEN TRUE
                ELSE FALSE
            END AS is_weekend
        FROM date_values
        ORDER BY date_value;
    """)

    print("Created table: dim_date")

    # Dimension: Queue
    con.execute("""
        CREATE OR REPLACE TABLE dim_queue AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY queue_clean) AS queue_key,
            queue_clean,
            MIN(queue) AS queue_original,
            COUNT(*) AS total_tickets_in_queue
        FROM silver_support_tickets
        GROUP BY queue_clean
        ORDER BY queue_key;
    """)

    print("Created table: dim_queue")

    # Dimension: Priority
    con.execute("""
        CREATE OR REPLACE TABLE dim_priority AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY priority_clean) AS priority_key,
            priority_clean,
            MIN(priority) AS priority_original,
            MIN(sla_target_hours) AS sla_target_hours,
            COUNT(*) AS total_tickets_with_priority
        FROM silver_support_tickets
        GROUP BY priority_clean
        ORDER BY priority_key;
    """)

    print("Created table: dim_priority")

    # Dimension: Language
    con.execute("""
        CREATE OR REPLACE TABLE dim_language AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY language_clean) AS language_key,
            language_clean,
            MIN(language) AS language_original,
            COUNT(*) AS total_tickets_in_language
        FROM silver_support_tickets
        GROUP BY language_clean
        ORDER BY language_key;
    """)

    print("Created table: dim_language")

    # Dimension: Agent
    con.execute("""
        CREATE OR REPLACE TABLE dim_agent AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY agent_name) AS agent_key,
            agent_name,
            COUNT(*) AS total_assigned_tickets
        FROM silver_support_tickets
        GROUP BY agent_name
        ORDER BY agent_key;
    """)

    print("Created table: dim_agent")

    # Dimension: Ticket Category
    con.execute("""
        CREATE OR REPLACE TABLE dim_ticket_category AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY ticket_category_rule_based) AS category_key,
            ticket_category_rule_based AS ticket_category,
            COUNT(*) AS total_tickets_in_category
        FROM silver_support_tickets
        GROUP BY ticket_category_rule_based
        ORDER BY category_key;
    """)

    print("Created table: dim_ticket_category")

    # Dimension: Status
    con.execute("""
        CREATE OR REPLACE TABLE dim_status AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY status) AS status_key,
            status,
            COUNT(*) AS total_tickets_with_status
        FROM silver_support_tickets
        GROUP BY status
        ORDER BY status_key;
    """)

    print("Created table: dim_status")

    # Dimension: Type
    con.execute("""
        CREATE OR REPLACE TABLE dim_type AS
        SELECT
            ROW_NUMBER() OVER (ORDER BY type_clean) AS type_key,
            type_clean,
            MIN(type) AS type_original,
            COUNT(*) AS total_tickets_with_type
        FROM silver_support_tickets
        GROUP BY type_clean
        ORDER BY type_key;
    """)

    print("Created table: dim_type")

    # Fact Table
    con.execute("""
        CREATE OR REPLACE TABLE fact_support_tickets AS
        SELECT
            s.ticket_id,

            dc.date_key AS created_date_key,
            dr.date_key AS resolved_date_key,

            dq.queue_key,
            dp.priority_key,
            dl.language_key,
            da.agent_key,
            dcat.category_key,
            ds.status_key,
            dt.type_key,

            s.created_date,
            s.resolved_date,

            s.resolution_time_hours,
            s.sla_target_hours,

            s.combined_text_length,
            s.tag_count,

            CASE WHEN s.status = 'Closed' THEN 1 ELSE 0 END AS is_closed,
            CASE WHEN s.status = 'Open' THEN 1 ELSE 0 END AS is_open,
            CASE WHEN s.status = 'Pending' THEN 1 ELSE 0 END AS is_pending,
            CASE WHEN s.status = 'Escalated' THEN 1 ELSE 0 END AS is_escalated,

            CASE WHEN s.sla_status = 'SLA Met' THEN 1 ELSE 0 END AS is_sla_met,
            CASE WHEN s.sla_status = 'SLA Breached' THEN 1 ELSE 0 END AS is_sla_breached,

            s.has_subject,
            s.has_body,
            s.has_answer,
            s.is_operational_data_simulated

        FROM silver_support_tickets s

        LEFT JOIN dim_date dc
            ON CAST(s.created_date AS DATE) = dc.date_value

        LEFT JOIN dim_date dr
            ON CAST(s.resolved_date AS DATE) = dr.date_value

        LEFT JOIN dim_queue dq
            ON s.queue_clean = dq.queue_clean

        LEFT JOIN dim_priority dp
            ON s.priority_clean = dp.priority_clean

        LEFT JOIN dim_language dl
            ON s.language_clean = dl.language_clean

        LEFT JOIN dim_agent da
            ON s.agent_name = da.agent_name

        LEFT JOIN dim_ticket_category dcat
            ON s.ticket_category_rule_based = dcat.ticket_category

        LEFT JOIN dim_status ds
            ON s.status = ds.status

        LEFT JOIN dim_type dt
            ON s.type_clean = dt.type_clean;
    """)

    print("Created table: fact_support_tickets")


def create_validation_reports(con):
    """
    Creates validation reports for the Phase 3 star schema.
    """

    run_query_to_csv(
        con,
        """
        SELECT
            'silver_support_tickets' AS table_name,
            COUNT(*) AS row_count
        FROM silver_support_tickets

        UNION ALL

        SELECT
            'fact_support_tickets' AS table_name,
            COUNT(*) AS row_count
        FROM fact_support_tickets

        UNION ALL

        SELECT
            'dim_date' AS table_name,
            COUNT(*) AS row_count
        FROM dim_date

        UNION ALL

        SELECT
            'dim_queue' AS table_name,
            COUNT(*) AS row_count
        FROM dim_queue

        UNION ALL

        SELECT
            'dim_priority' AS table_name,
            COUNT(*) AS row_count
        FROM dim_priority

        UNION ALL

        SELECT
            'dim_language' AS table_name,
            COUNT(*) AS row_count
        FROM dim_language

        UNION ALL

        SELECT
            'dim_agent' AS table_name,
            COUNT(*) AS row_count
        FROM dim_agent

        UNION ALL

        SELECT
            'dim_ticket_category' AS table_name,
            COUNT(*) AS row_count
        FROM dim_ticket_category

        UNION ALL

        SELECT
            'dim_status' AS table_name,
            COUNT(*) AS row_count
        FROM dim_status

        UNION ALL

        SELECT
            'dim_type' AS table_name,
            COUNT(*) AS row_count
        FROM dim_type;
        """,
        "phase3_table_row_counts.csv"
    )

    run_query_to_csv(
        con,
        """
        SELECT
            COUNT(*) AS total_fact_rows,
            COUNT(DISTINCT ticket_id) AS unique_ticket_ids,
            COUNT(*) - COUNT(DISTINCT ticket_id) AS duplicate_ticket_ids,
            SUM(CASE WHEN created_date_key IS NULL THEN 1 ELSE 0 END) AS missing_created_date_key,
            SUM(CASE WHEN queue_key IS NULL THEN 1 ELSE 0 END) AS missing_queue_key,
            SUM(CASE WHEN priority_key IS NULL THEN 1 ELSE 0 END) AS missing_priority_key,
            SUM(CASE WHEN language_key IS NULL THEN 1 ELSE 0 END) AS missing_language_key,
            SUM(CASE WHEN agent_key IS NULL THEN 1 ELSE 0 END) AS missing_agent_key,
            SUM(CASE WHEN category_key IS NULL THEN 1 ELSE 0 END) AS missing_category_key,
            SUM(CASE WHEN status_key IS NULL THEN 1 ELSE 0 END) AS missing_status_key,
            SUM(CASE WHEN type_key IS NULL THEN 1 ELSE 0 END) AS missing_type_key
        FROM fact_support_tickets;
        """,
        "phase3_fact_validation.csv"
    )

    run_query_to_csv(
        con,
        """
        SELECT
            ds.status,
            COUNT(*) AS ticket_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
        FROM fact_support_tickets f
        LEFT JOIN dim_status ds
            ON f.status_key = ds.status_key
        GROUP BY ds.status
        ORDER BY ticket_count DESC;
        """,
        "phase3_status_distribution_from_model.csv"
    )

    run_query_to_csv(
        con,
        """
        SELECT
            dq.queue_clean,
            COUNT(*) AS ticket_count,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(f.is_sla_breached) AS sla_breached_tickets
        FROM fact_support_tickets f
        LEFT JOIN dim_queue dq
            ON f.queue_key = dq.queue_key
        GROUP BY dq.queue_clean
        ORDER BY ticket_count DESC;
        """,
        "phase3_queue_performance_from_model.csv"
    )

    run_query_to_csv(
        con,
        """
        SELECT
            dcat.ticket_category,
            COUNT(*) AS ticket_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage,
            ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
            SUM(f.is_sla_breached) AS sla_breached_tickets
        FROM fact_support_tickets f
        LEFT JOIN dim_ticket_category dcat
            ON f.category_key = dcat.category_key
        GROUP BY dcat.ticket_category
        ORDER BY ticket_count DESC;
        """,
        "phase3_category_performance_from_model.csv"
    )


def create_markdown_report(con):
    """
    Creates Phase 3 markdown documentation report.
    """

    row_counts = con.execute("""
        SELECT
            'fact_support_tickets' AS table_name,
            COUNT(*) AS row_count
        FROM fact_support_tickets

        UNION ALL

        SELECT
            'dim_date' AS table_name,
            COUNT(*) AS row_count
        FROM dim_date

        UNION ALL

        SELECT
            'dim_queue' AS table_name,
            COUNT(*) AS row_count
        FROM dim_queue

        UNION ALL

        SELECT
            'dim_priority' AS table_name,
            COUNT(*) AS row_count
        FROM dim_priority

        UNION ALL

        SELECT
            'dim_language' AS table_name,
            COUNT(*) AS row_count
        FROM dim_language

        UNION ALL

        SELECT
            'dim_agent' AS table_name,
            COUNT(*) AS row_count
        FROM dim_agent

        UNION ALL

        SELECT
            'dim_ticket_category' AS table_name,
            COUNT(*) AS row_count
        FROM dim_ticket_category

        UNION ALL

        SELECT
            'dim_status' AS table_name,
            COUNT(*) AS row_count
        FROM dim_status

        UNION ALL

        SELECT
            'dim_type' AS table_name,
            COUNT(*) AS row_count
        FROM dim_type;
    """).df()

    validation = con.execute("""
        SELECT
            COUNT(*) AS total_fact_rows,
            COUNT(DISTINCT ticket_id) AS unique_ticket_ids,
            COUNT(*) - COUNT(DISTINCT ticket_id) AS duplicate_ticket_ids,
            SUM(CASE WHEN created_date_key IS NULL THEN 1 ELSE 0 END) AS missing_created_date_key,
            SUM(CASE WHEN queue_key IS NULL THEN 1 ELSE 0 END) AS missing_queue_key,
            SUM(CASE WHEN priority_key IS NULL THEN 1 ELSE 0 END) AS missing_priority_key,
            SUM(CASE WHEN language_key IS NULL THEN 1 ELSE 0 END) AS missing_language_key,
            SUM(CASE WHEN agent_key IS NULL THEN 1 ELSE 0 END) AS missing_agent_key,
            SUM(CASE WHEN category_key IS NULL THEN 1 ELSE 0 END) AS missing_category_key,
            SUM(CASE WHEN status_key IS NULL THEN 1 ELSE 0 END) AS missing_status_key,
            SUM(CASE WHEN type_key IS NULL THEN 1 ELSE 0 END) AS missing_type_key
        FROM fact_support_tickets;
    """).df()

    report = f"""
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

{row_counts.to_markdown(index=False)}

## Fact Table Validation

{validation.to_markdown(index=False)}

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
"""

    report_path = REPORT_DIR / "phase3_sql_data_model_report.md"
    report_path.write_text(report.strip(), encoding="utf-8")
    print(f"Saved markdown report: {report_path}")


def main():
    if not SILVER_FILE.exists():
        raise FileNotFoundError(
            "Silver dataset not found. Complete Phase 2 before running Phase 3."
        )

    con = duckdb.connect(str(GOLD_DB))

    print("Creating Phase 3 star schema...")
    create_star_schema(con)

    print("Creating Phase 3 validation reports...")
    create_validation_reports(con)

    print("Creating Phase 3 markdown report...")
    create_markdown_report(con)

    con.close()

    print("Phase 3 SQL data model created successfully.")
    print(f"DuckDB database created here: {GOLD_DB}")


if __name__ == "__main__":
    main()
