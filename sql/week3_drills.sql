-- Week 3 SQL Drills — CTEs & JOINs
-- Date: 6 June 2026
-- Topics: INNER JOIN, LEFT JOIN, COALESCE, CTEs, multiple CTEs, CROSS JOIN

-- Dataset:
-- customers(customer_id, name, country)
-- orders(order_id, customer_id, amount, status)

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 1 — LEFT JOIN + COALESCE
-- Return each customer's name and total amount spent.
-- Include all customers. Show 0 for customers with no orders.
-- ─────────────────────────────────────────────────────────────────────────────

SELECT customers.name, COALESCE(SUM(orders.amount), 0) AS total_spent
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.name;

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 2 — INNER JOIN + filter
-- Return names and order amounts for all completed orders by UK customers only.
-- ─────────────────────────────────────────────────────────────────────────────

SELECT customers.name, orders.amount
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
WHERE customers.country = 'UK'
AND orders.status = 'completed';

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 3 — CTE
-- CTE: total amount spent per customer.
-- Main query: return only customers who spent more than 400 in total.
-- ─────────────────────────────────────────────────────────────────────────────

WITH total_spent AS (
    SELECT orders.customer_id, SUM(orders.amount) AS amount
    FROM orders
    GROUP BY orders.customer_id
)
SELECT customers.name, total_spent.amount
FROM customers
JOIN total_spent ON customers.customer_id = total_spent.customer_id
WHERE total_spent.amount > 400;

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 4 — CTE + JOIN
-- CTE: number of completed orders per country.
-- Main query: return only countries with more than one completed order.
-- ─────────────────────────────────────────────────────────────────────────────

WITH completed_country AS (
    SELECT customers.country, COUNT(orders.order_id) AS status_count
    FROM customers
    INNER JOIN orders ON customers.customer_id = orders.customer_id
    WHERE orders.status = 'completed'
    GROUP BY customers.country
)
SELECT completed_country.country
FROM completed_country
WHERE completed_country.status_count > 1;

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 5 — Two CTEs + CROSS JOIN
-- CTE 1: total spend per customer.
-- CTE 2: average total spend across all customers.
-- Main query: customers whose total spend is above the average.
-- ─────────────────────────────────────────────────────────────────────────────

WITH customer_spend AS (
    SELECT customer_id, SUM(amount) AS total_spend
    FROM orders
    GROUP BY customer_id
),
average_spend AS (
    SELECT AVG(total_spend) AS avg_spend
    FROM customer_spend
)
SELECT c.name, cs.total_spend
FROM customers c
JOIN customer_spend cs ON c.customer_id = cs.customer_id
CROSS JOIN average_spend a
WHERE cs.total_spend > a.avg_spend;
