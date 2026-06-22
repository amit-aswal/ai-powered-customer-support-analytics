-- Phase 1: Raw Customer Support Ticket Profiling
-- SQL Engine: DuckDB

CREATE OR REPLACE VIEW raw_support_tickets AS
SELECT *
FROM read_parquet('data/bronze/support_tickets_raw.parquet');


-- 1. Total tickets

SELECT
    COUNT(*) AS total_tickets
FROM raw_support_tickets;


-- 2. Ticket type distribution

SELECT
    "type",
    COUNT(*) AS ticket_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
FROM raw_support_tickets
GROUP BY "type"
ORDER BY ticket_count DESC;


-- 3. Queue distribution

SELECT
    queue,
    COUNT(*) AS ticket_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
FROM raw_support_tickets
GROUP BY queue
ORDER BY ticket_count DESC;


-- 4. Priority distribution

SELECT
    priority,
    COUNT(*) AS ticket_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
FROM raw_support_tickets
GROUP BY priority
ORDER BY ticket_count DESC;


-- 5. Language distribution

SELECT
    language,
    COUNT(*) AS ticket_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
FROM raw_support_tickets
GROUP BY language
ORDER BY ticket_count DESC;


-- 6. Queue and priority workload matrix

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


-- 7. Missing key text fields

SELECT
    COUNT(*) AS total_rows,

    SUM(CASE WHEN subject IS NULL OR TRIM(subject) = '' THEN 1 ELSE 0 END) AS missing_subject,
    SUM(CASE WHEN body IS NULL OR TRIM(body) = '' THEN 1 ELSE 0 END) AS missing_body,
    SUM(CASE WHEN answer IS NULL OR TRIM(answer) = '' THEN 1 ELSE 0 END) AS missing_answer
FROM raw_support_tickets;


-- 8. Possible duplicate tickets

SELECT
    subject,
    body,
    COUNT(*) AS duplicate_count
FROM raw_support_tickets
GROUP BY subject, body
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;


-- 9. Text length profile

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


-- 10. Top queues by ticket volume using CTE and ranking

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
