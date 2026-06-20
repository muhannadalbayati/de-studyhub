-- Week 4 SQL Drills — Window Functions
-- Date: 20 June 2026
-- Topics: RANK, SUM() OVER running totals, LAG, PARTITION BY

-- Dataset:
-- customers(customer_id, name, country)
-- orders(order_id, customer_id, amount, order_date)

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 1 — Global rank by amount
-- Show every order with its amount and a global rank — highest first.
-- ─────────────────────────────────────────────────────────────────────────────

SELECT
    order_id,
    amount,
    RANK() OVER (ORDER BY amount DESC) AS rank
FROM orders;

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 2 — Rank within each customer
-- Show every order with its rank within its customer — highest first.
-- ─────────────────────────────────────────────────────────────────────────────

SELECT
    c.name,
    o.order_id,
    o.amount,
    RANK() OVER (PARTITION BY c.customer_id ORDER BY o.amount DESC) AS customer_rank
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 3 — Running total
-- Show each order with its amount and the running total ordered by date.
-- ─────────────────────────────────────────────────────────────────────────────

SELECT
    c.name,
    o.order_id,
    o.order_date,
    o.amount,
    SUM(o.amount) OVER (ORDER BY o.order_date) AS running_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 4 — LAG: previous order amount
-- Show each order with its amount and the previous order's amount by date.
-- First row returns NULL for previous_amount.
-- ─────────────────────────────────────────────────────────────────────────────

SELECT
    c.name,
    o.order_id,
    o.order_date,
    o.amount,
    LAG(o.amount, 1) OVER (ORDER BY o.order_date) AS previous_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- ─────────────────────────────────────────────────────────────────────────────
-- Drill 5 — CTE + RANK within country
-- Show each customer's name, total spend, and rank within their country.
-- Highest spender per country gets rank 1.
-- ─────────────────────────────────────────────────────────────────────────────

WITH customer_spend AS (
    SELECT
        c.customer_id,
        c.name,
        c.country,
        SUM(o.amount) AS total_spend
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name, c.country
)
SELECT
    name,
    country,
    total_spend,
    RANK() OVER (PARTITION BY country ORDER BY total_spend DESC) AS country_rank
FROM customer_spend;
