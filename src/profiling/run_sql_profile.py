from pathlib import Path
import duckdb


BRONZE_FILE = "data/bronze/support_tickets_raw.parquet"
REPORT_DIR = Path("reports/sql_outputs")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def run_query_and_save(connection, query: str, output_file: str) -> None:
    df = connection.execute(query).df()
    output_path = REPORT_DIR / output_file
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Saved: {output_path}")


def main():
    con = duckdb.connect()

    con.execute(f"""
        CREATE OR REPLACE VIEW raw_support_tickets AS
        SELECT *
        FROM read_parquet('{BRONZE_FILE}');
    """)

    queries = {
        "sql_total_tickets.csv": """
            SELECT
                COUNT(*) AS total_tickets
            FROM raw_support_tickets;
        """,

        "sql_type_distribution.csv": """
            SELECT
                "type",
                COUNT(*) AS ticket_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
            FROM raw_support_tickets
            GROUP BY "type"
            ORDER BY ticket_count DESC;
        """,

        "sql_queue_distribution.csv": """
            SELECT
                queue,
                COUNT(*) AS ticket_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
            FROM raw_support_tickets
            GROUP BY queue
            ORDER BY ticket_count DESC;
        """,

        "sql_priority_distribution.csv": """
            SELECT
                priority,
                COUNT(*) AS ticket_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
            FROM raw_support_tickets
            GROUP BY priority
            ORDER BY ticket_count DESC;
        """,

        "sql_language_distribution.csv": """
            SELECT
                language,
                COUNT(*) AS ticket_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
            FROM raw_support_tickets
            GROUP BY language
            ORDER BY ticket_count DESC;
        """,

        "sql_queue_priority_matrix.csv": """
            SELECT
                queue,
                priority,
                COUNT(*) AS ticket_count,
                RANK() OVER (
                    PARTITION BY queue
                    ORDER BY COUNT(*) DESC
                ) AS priority_rank_within_queue
            FROM raw_support_tickets
            GROUP BY queue, priority
            ORDER BY queue, ticket_count DESC;
        """,

        "sql_missing_text_fields.csv": """
            SELECT
                COUNT(*) AS total_rows,
                SUM(CASE WHEN subject IS NULL OR TRIM(subject) = '' THEN 1 ELSE 0 END) AS missing_subject,
                SUM(CASE WHEN body IS NULL OR TRIM(body) = '' THEN 1 ELSE 0 END) AS missing_body,
                SUM(CASE WHEN answer IS NULL OR TRIM(answer) = '' THEN 1 ELSE 0 END) AS missing_answer
            FROM raw_support_tickets;
        """,

        "sql_text_length_profile.csv": """
            SELECT
                MIN(LENGTH(subject)) AS min_subject_length,
                AVG(LENGTH(subject)) AS avg_subject_length,
                MAX(LENGTH(subject)) AS max_subject_length,

                MIN(LENGTH(body)) AS min_body_length,
                AVG(LENGTH(body)) AS avg_body_length,
                MAX(LENGTH(body)) AS max_body_length,

                MIN(LENGTH(answer)) AS min_answer_length,
                AVG(LENGTH(answer)) AS avg_answer_length,
                MAX(LENGTH(answer)) AS max_answer_length
            FROM raw_support_tickets;
        """,

        "sql_top_queues_ranked.csv": """
            WITH queue_volume AS (
                SELECT
                    queue,
                    COUNT(*) AS ticket_count
                FROM raw_support_tickets
                GROUP BY queue
            ),

            ranked_queues AS (
                SELECT
                    queue,
                    ticket_count,
                    RANK() OVER (ORDER BY ticket_count DESC) AS queue_rank
                FROM queue_volume
            )

            SELECT
                queue_rank,
                queue,
                ticket_count
            FROM ranked_queues
            ORDER BY queue_rank;
        """
    }

    for output_file, query in queries.items():
        run_query_and_save(con, query, output_file)

    con.close()

    print("SQL profiling completed successfully.")


if __name__ == "__main__":
    main()
