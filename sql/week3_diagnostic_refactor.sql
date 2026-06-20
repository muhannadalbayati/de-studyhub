-- Week 3 — Diagnostic Query Refactor
-- Date: 6 June 2026
-- Task: Rewrite the original Week 1 diagnostic query using CTEs instead of a subquery.
-- Original query had 4 errors and used an unnecessary subquery — now refactored to CTE pattern.

-- ─────────────────────────────────────────────────────────────────────────────
-- Returns countries where customers have placed more than one order
-- with a total over 100, ordered by order count descending.
-- ─────────────────────────────────────────────────────────────────────────────

WITH high_value_orders AS (
    SELECT customers.country, orders.order_id
    FROM customers
    JOIN orders ON customers.id = orders.customer_id
    WHERE orders.total > 100
),
country_order_counts AS (
    SELECT country, COUNT(*) AS order_count
    FROM high_value_orders
    GROUP BY country
)
SELECT country, order_count
FROM country_order_counts
WHERE order_count > 1
ORDER BY order_count DESC;
