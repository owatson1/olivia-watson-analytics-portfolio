import duckdb
import os

con = duckdb.connect('/Users/oliviawatson/Desktop/Cowork/Project 2/Analysis/olist.duckdb')
out = '/Users/oliviawatson/Desktop/Cowork/Project 2/Analysis/outputs'
os.makedirs(out, exist_ok=True)

# Monthly GMV trend
df = con.execute("""
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS order_month,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(oi.price), 2) AS gmv,
        ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY order_month
    ORDER BY order_month
""").df()
df.to_csv(f'{out}/monthly_trend.csv', index=False)
print(f'monthly_trend.csv: {len(df)} rows')

# Category revenue top 10
df = con.execute("""
    SELECT
        COALESCE(ct.product_category_name_english, p.product_category_name) AS category,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        ROUND(SUM(oi.price), 2) AS revenue,
        ROUND(AVG(oi.price), 2) AS avg_item_price
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
    WHERE o.order_status = 'delivered'
    GROUP BY category
    ORDER BY revenue DESC
    LIMIT 10
""").df()
df.to_csv(f'{out}/category_revenue.csv', index=False)
print(f'category_revenue.csv: {len(df)} rows')

# Delivery by state
df = con.execute("""
    SELECT
        s.seller_state,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 1 ELSE 0 END) AS on_time_orders,
        ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 1 ELSE 0 END) / COUNT(DISTINCT o.order_id), 2) AS on_time_pct
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN sellers s ON oi.seller_id = s.seller_id
    WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL
    GROUP BY s.seller_state
    HAVING COUNT(DISTINCT o.order_id) >= 50
    ORDER BY on_time_pct DESC
""").df()
df.to_csv(f'{out}/delivery_by_state.csv', index=False)
print(f'delivery_by_state.csv: {len(df)} rows')

# Review distribution
df = con.execute("""
    SELECT
        r.review_score,
        COUNT(*) AS review_count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
    FROM order_reviews r
    JOIN orders o ON r.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY r.review_score
    ORDER BY r.review_score
""").df()
df.to_csv(f'{out}/review_distribution.csv', index=False)
print(f'review_distribution.csv: {len(df)} rows')

# KPI summary
df = con.execute("""
    SELECT
        ROUND(SUM(oi.price), 2) AS total_gmv,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value,
        ROUND(100.0 * SUM(CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 1 ELSE 0 END) / COUNT(DISTINCT o.order_id), 2) AS on_time_delivery_pct,
        ROUND(AVG(r.review_score), 2) AS avg_review_score
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL
""").df()
df.to_csv(f'{out}/kpi_summary.csv', index=False)
print(f'kpi_summary.csv: {len(df)} rows')

con.close()
print('All Page 1 outputs exported successfully.')