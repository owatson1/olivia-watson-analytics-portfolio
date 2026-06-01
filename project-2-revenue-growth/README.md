# Project 2: Revenue & Growth Analytics
### Olist Brazilian E-Commerce: Commercial Performance & Market Opportunity

---

## The Question

Many e-commerce dashboards show you total revenue and call it a day. This project asks something harder: where is the revenue actually coming from, what's driving customer satisfaction, and, more importantly, where is growth being left on the table?

Using 100K+ real transactions from Olist, Brazil's largest online marketplace (similar to Amazon in the US), I built a two-page commercial analytics dashboard that moves from performance measurement to strategic opportunity sizing.

---

## What I Built

### Page 1: Commercial Performance
A senior leadership view of the core business: revenue trends, category performance, fulfillment reliability, and customer satisfaction patterns. This is meant to be basic. It focuses on key metrics to set the stage before diving deeper.

**Key findings:**
- GMV grew from ~$300K/month in early 2017 to ~$1M/month by November 2017, driven by a clear holiday season spike
- Health & Beauty and Watches & Gifts lead revenue, together accounting for nearly $2.4M, or 18% of total GMV
- 91.9% of orders are delivered on time nationally, but MA sits at 76.9%. This is a significant outlier that correlates with lower review scores
- Review scores are bimodal: 58% are 5-star, BUT 11% are 1-star. The middle is thin. Delivery experience is most likely the dividing factor.

### Page 2: Where to Grow *(coming soon)*
A market opportunity analysis that merges Olist transaction data with Brazilian state-level economic data (IBGE, 2017) to identify where e-commerce revenue is undertapped relative to regional wealth and population. Data means nothing unless we can anchor it to something. This merge allows us to see the data benchmarked against National data.

Planned analysis includes:
- Regional opportunity matrix: GMV per capita vs. GDP per capita by state
- Repeat purchase rate by state — retention proxy across the customer base
- Cohort LTV analysis: how much did each monthly acquisition cohort spend over time?
- Fulfillment speed vs. review score correlation: does faster delivery actually drive satisfaction?

---

## Tools & Approach

| Layer | Tool |
|---|---|
| Data storage | DuckDB |
| Data transformation | Python, SQL |
| Visualization | Tableau Public |
| Environment | VS Code, Terminal |

All analysis was written in SQL and Python. Queries use window functions, CTEs, and multi-table joins across 9 normalized source tables.

---

## Data Sources

- **Transaction data:** [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Kaggle, 9 CSV files, 100K+ orders (2016–2018)
- **State economic data:** IBGE Regional Accounts of Brazil, 2017. Brazilian Institute of Geography and Statistics (ibge.gov.br). Values compiled from published tables.

---

## Live Dashboard _
Note: Dashboard 1 is LIVE, Dashboard 2 coming soon :)_

[View on Tableau Public](https://public.tableau.com/app/profile/olivia.watson4893/viz/OlistCommercialGrowthAnalytics_OliviaWatson/Dashboard1)

---

## Repository Structure

```
project-2-revenue-growth/
├── README.md
├── Analysis/
│   ├── scripts/
│   │   ├── 01_commercial_performance.sql
│   │   ├── 02_export_performance.py
│   │   ├── 03_growth_opportunity.sql
│   │   └── 04_export_growth.py
│   └── outputs/
│       ├── monthly_trend.csv
│       ├── category_revenue.csv
│       ├── delivery_by_state.csv
│       ├── review_distribution.csv
│       ├── kpi_summary.csv
│       ├── repeat_rate_by_state.csv
│       ├── regional_opportunity.csv
│       ├── cohort_ltv.csv
│       └── fulfillment_vs_satisfaction.csv
```

---

## Assumptions & Limitations

- Analysis is filtered to **delivered orders only**. Canceled, unavailable, and in-progress orders are excluded from all revenue and satisfaction metrics
- On-time delivery is defined as: `order_delivered_customer_date <= order_estimated_delivery_date`
- The dataset ends in October 2018 and begins in September 2016. 2017 is the only complete calendar year and serves as the primary baseline
- Repeat purchase rate (3%) reflects Olist's marketplace model, where most buyers arrive via search rather than direct loyalty — this is a characteristic of the platform, not a data quality issue
- State economic data is from 2017 to align with the peak transaction period in the dataset

---

*Last updated: May 2026 | Tools: DuckDB, SQL, Python, Tableau Public*
