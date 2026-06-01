import duckdb
import os

con = duckdb.connect('/Users/oliviawatson/Desktop/Cowork/Project 2/Analysis/olist.duckdb')
out = '/Users/oliviawatson/Desktop/Cowork/Project 2/Analysis/outputs'
os.makedirs(out, exist_ok=True)

# Repeat purchase rate by state
df = con.execute("""
    SELECT
        c.customer_state,
        COUNT(DISTINCT c.customer_unique_id) AS total_customers,
        SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
        ROUND(100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)
              / COUNT(DISTINCT c.customer_unique_id), 2) AS repeat_rate_pct
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
    ORDER BY repeat_rate_pct DESC
""").df()
df.to_csv(f'{out}/repeat_rate_by_state.csv', index=False)
print(f'repeat_rate_by_state.csv: {len(df)} rows')

# Regional opportunity matrix
df = con.execute("""
    SELECT
        c.customer_state,
        e.state_name,
        e.region,
        e.population_2017,
        e.gdp_per_capita_2017_brl,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(oi.price), 2) AS total_gmv,
        ROUND(SUM(oi.price) / e.population_2017 * 1000, 2) AS gmv_per_1000_population
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN brazil_state_economics e ON c.customer_state = e.state_code
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_state, e.state_name, e.region, e.population_2017, e.gdp_per_capita_2017_brl
    ORDER BY gmv_per_1000_population DESC
""").df()
df.to_csv(f'{out}/regional_opportunity.csv', index=False)
print(f'regional_opportunity.csv: {len(df)} rows')

# Cohort LTV
df = con.execute("""
    WITH first_orders AS (
        SELECT c.customer_unique_id,
            DATE_TRUNC('month', MIN(o.order_purchase_timestamp))::DATE AS cohort_month
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_status = 'delivered'
        GROUP BY c.customer_unique_id
    ),
    customer_revenue AS (
        SELECT c.customer_unique_id,
            DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS order_month,
            SUM(oi.price) AS revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY c.customer_unique_id, order_month
    )
    SELECT
        f.cohort_month,
        COUNT(DISTINCT f.customer_unique_id) AS cohort_size,
        ROUND(SUM(r.revenue), 2) AS total_cohort_revenue,
        ROUND(SUM(r.revenue) / COUNT(DISTINCT f.customer_unique_id), 2) AS ltv_per_customer
    FROM first_orders f
    JOIN customer_revenue r ON f.customer_unique_id = r.customer_unique_id
    WHERE f.cohort_month >= '2017-01-01'
    AND f.cohort_month < '2018-09-01'
    GROUP BY f.cohort_month
    ORDER BY f.cohort_month
""").df()
df.to_csv(f'{out}/cohort_ltv.csv', index=False)
print(f'cohort_ltv.csv: {len(df)} rows')

# Fulfillment speed vs review score
df = con.execute("""
    SELECT
        s.seller_state,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(AVG(DATEDIFF('day', o.order_purchase_timestamp, o.order_delivered_customer_date)), 1) AS avg_delivery_days,
        ROUND(AVG(r.review_score), 2) AS avg_review_score
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN sellers s ON oi.seller_id = s.seller_id
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY s.seller_state
    HAVING COUNT(DISTINCT o.order_id) >= 50
    ORDER BY avg_delivery_days
""").df()
df.to_csv(f'{out}/fulfillment_vs_satisfaction.csv', index=False)
print(f'fulfillment_vs_satisfaction.csv: {len(df)} rows')

con.close()
print('All Page 2 outputs exported successfully.')