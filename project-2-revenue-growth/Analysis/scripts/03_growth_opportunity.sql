-- ============================================================
-- Project 2: Revenue & Growth Analytics
-- Script 03: Growth & Opportunity Analysis
-- Feeds: Page 2 of Tableau dashboard
-- ============================================================


-- ============================================================
-- SECTION 1: Repeat Purchase Rate by Customer State
-- Chart: Horizontal bar — retention proxy by state
-- A customer is "repeat" if they placed more than 1 order
-- using the same unique customer ID
-- ============================================================

SELECT
    c.customer_state,
    COUNT(DISTINCT c.customer_unique_id)                                        AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)                           AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)
          / COUNT(DISTINCT c.customer_unique_id), 2)                            AS repeat_rate_pct
FROM customers c
JOIN (
    SELECT c2.customer_unique_id, COUNT(DISTINCT o.order_id) AS order_count
    FROM orders o
    JOIN customers c2 ON o.customer_id = c2.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c2.customer_unique_id
) repeat_data ON c.customer_unique_id = repeat_data.customer_unique_id
GROUP BY c.customer_state
HAVING COUNT(DISTINCT c.customer_unique_id) >= 100
ORDER BY repeat_rate_pct DESC;


-- ============================================================
-- SECTION 2: Regional Opportunity Matrix
-- Chart: Scatter plot — GMV per capita vs GDP per capita by state
-- This is the economic merge — the "edge" chart
-- High GDP, low GMV per capita = underserved market opportunity
-- ============================================================

SELECT
    c.customer_state,
    e.state_name,
    e.region,
    e.population_2017,
    e.gdp_per_capita_2017_brl,
    COUNT(DISTINCT o.order_id)                                                  AS total_orders,
    ROUND(SUM(oi.price), 2)                                                     AS total_gmv,
    ROUND(SUM(oi.price) / e.population_2017 * 1000, 2)                         AS gmv_per_1000_population
FROM orders o
JOIN customers c        ON o.customer_id = c.customer_id
JOIN order_items oi     ON o.order_id = oi.order_id
JOIN brazil_state_economics e ON c.customer_state = e.state_code
WHERE o.order_status = 'delivered'
GROUP BY
    c.customer_state,
    e.state_name,
    e.region,
    e.population_2017,
    e.gdp_per_capita_2017_brl
ORDER BY gmv_per_1000_population DESC;


-- ============================================================
-- SECTION 3: Cohort LTV Analysis
-- Chart: Line — cumulative revenue by first-order cohort month
-- Shows how much each monthly cohort spent over time
-- ============================================================

WITH first_orders AS (
    SELECT
        c.customer_unique_id,
        DATE_TRUNC('month', MIN(o.order_purchase_timestamp))::DATE AS cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
customer_revenue AS (
    SELECT
        c.customer_unique_id,
        DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS order_month,
        SUM(oi.price) AS revenue
    FROM orders o
    JOIN customers c    ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id, order_month
)
SELECT
    f.cohort_month,
    COUNT(DISTINCT f.customer_unique_id)                            AS cohort_size,
    ROUND(SUM(r.revenue), 2)                                        AS total_cohort_revenue,
    ROUND(SUM(r.revenue) / COUNT(DISTINCT f.customer_unique_id), 2) AS ltv_per_customer
FROM first_orders f
JOIN customer_revenue r ON f.customer_unique_id = r.customer_unique_id
WHERE f.cohort_month >= '2017-01-01'
AND f.cohort_month < '2018-09-01'
GROUP BY f.cohort_month
ORDER BY f.cohort_month;


-- ============================================================
-- SECTION 4: Fulfillment Speed vs Review Score
-- Chart: Scatter — delivery days vs avg review score by seller
-- Does faster delivery actually drive satisfaction?
-- ============================================================

SELECT
    s.seller_state,
    COUNT(DISTINCT o.order_id)                                                  AS total_orders,
    ROUND(AVG(
        DATEDIFF('day',
            o.order_purchase_timestamp,
            o.order_delivered_customer_date)
    ), 1)                                                                       AS avg_delivery_days,
    ROUND(AVG(r.review_score), 2)                                               AS avg_review_score
FROM orders o
JOIN order_items oi      ON o.order_id = oi.order_id
JOIN sellers s           ON oi.seller_id = s.seller_id
JOIN order_reviews r     ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
AND o.order_delivered_customer_date IS NOT NULL
GROUP BY s.seller_state
HAVING COUNT(DISTINCT o.order_id) >= 50
ORDER BY avg_delivery_days;