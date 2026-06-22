-- Phase 3: Business KPI Analytics Queries
-- SQL Engine: DuckDB
-- Database: data/gold/customer_support_analytics.duckdb

-- 1. Executive KPI Summary

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


-- 2. Ticket Volume by Status

SELECT
    ds.status,
    COUNT(*) AS ticket_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage
FROM fact_support_tickets f
LEFT JOIN dim_status ds
    ON f.status_key = ds.status_key
GROUP BY ds.status
ORDER BY ticket_count DESC;


-- 3. Queue Performance

SELECT
    dq.queue_clean,
    COUNT(*) AS total_tickets,
    SUM(f.is_closed) AS closed_tickets,
    SUM(f.is_open) AS open_tickets,
    ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours,
    SUM(f.is_sla_breached) AS sla_breached_tickets,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS workload_rank
FROM fact_support_tickets f
LEFT JOIN dim_queue dq
    ON f.queue_key = dq.queue_key
GROUP BY dq.queue_clean
ORDER BY total_tickets DESC;


-- 4. Priority SLA Performance

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


-- 5. Agent Performance

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


-- 6. Ticket Category Analysis

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


-- 7. Monthly Ticket Trend

SELECT
    dd.year,
    dd.month_number,
    dd.month_name,
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


-- 8. Month-over-Month Ticket Growth

WITH monthly_tickets AS (
    SELECT
        dd.year,
        dd.month_number,
        dd.month_name,
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


-- 9. Language Distribution

SELECT
    dl.language_clean,
    COUNT(*) AS total_tickets,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS ticket_percentage,
    ROUND(AVG(f.resolution_time_hours), 2) AS avg_resolution_time_hours
FROM fact_support_tickets f
LEFT JOIN dim_language dl
    ON f.language_key = dl.language_key
GROUP BY dl.language_clean
ORDER BY total_tickets DESC;


-- 10. Top SLA Breach Drivers

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
