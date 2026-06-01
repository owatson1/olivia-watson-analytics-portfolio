-- ============================================================
-- Project 2: Revenue & Growth Analytics
-- Script 01: Commercial Performance
-- Feeds: Page 1 of Tableau dashboard
-- ============================================================

-- ============================================================
-- SECTION 1: Monthly GMV and Order Volume Trend
-- Chart: Dual line — GMV (primary) + order count (context)
-- Note: 2016 is partial (starts Sept). 2018 is partial (ends Oct).
-- Full baseline year is 2017.
-- ============================================================

SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS order_month,
    COUNT(DISTINCT o.order_id)                             AS total_orders,
    ROUND(SUM(oi.price), 2)                                AS gmv,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2)   AS avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY order_month
ORDER BY order_month;


-- ============================================================
-- SECTION 2: Revenue and Orders by Product Category
-- Chart: Horizontal bar — top 10 categories by revenue
-- ============================================================

SELECT
    COALESCE(ct.product_category_name_english, p.product_category_name) AS category,
    COUNT(DISTINCT oi.order_id)                                          AS total_orders,
    ROUND(SUM(oi.price), 2)                                              AS revenue,
    ROUND(AVG(oi.price), 2)                                              AS avg_item_price
FROM order_items oi
JOIN products p       ON oi.product_id = p.product_id
JOIN orders o         ON oi.order_id = o.order_id
LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY category
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- SECTION 3: On-Time Delivery Rate by Seller State
-- Chart: Map or horizontal bar
-- On-time = delivered on or before estimated delivery date
-- ============================================================

SELECT
    s.seller_state,
    COUNT(DISTINCT o.order_id)                                               AS total_orders,
    SUM(CASE WHEN o.order_delivered_customer_date
                  <= o.order_estimated_delivery_date THEN 1 ELSE 0 END)      AS on_time_orders,
    ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date
                  <= o.order_estimated_delivery_date THEN 1 ELSE 0 END)
          / COUNT(DISTINCT o.order_id), 2)                                   AS on_time_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN sellers s      ON oi.seller_id = s.seller_id
WHERE o.order_status = 'delivered'
AND o.order_delivered_customer_date IS NOT NULL
AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY s.seller_state
HAVING COUNT(DISTINCT o.order_id) >= 50  -- exclude states with very low volume
ORDER BY on_time_pct DESC;


-- ============================================================
-- SECTION 4: Review Score Distribution
-- Chart: Histogram / bar
-- Note: Bimodal — heavy 5-star with notable 1-star spike.
-- Annotate this in Tableau.
-- ============================================================

SELECT
    r.review_score,
    COUNT(*)                                            AS review_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM order_reviews r
JOIN orders o ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY r.review_score
ORDER BY r.review_score;


-- ============================================================
-- SECTION 5: KPI Summary Row
-- Feeds the 5 KPI tiles at the top of Page 1
-- ============================================================

SELECT
    ROUND(SUM(oi.price), 2)                                                   AS total_gmv,
    COUNT(DISTINCT o.order_id)                                                 AS total_orders,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2)                       AS avg_order_value,
    ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date
                  <= o.order_estimated_delivery_date THEN 1 ELSE 0 END)
          / COUNT(DISTINCT o.order_id), 2)                                     AS on_time_delivery_pct,
    ROUND(AVG(r.review_score), 2)                                              AS avg_review_score
FROM orders o
JOIN order_items oi  ON o.order_id = oi.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
AND o.order_delivered_customer_date IS NOT NULL
AND o.order_estimated_delivery_date IS NOT NULL;