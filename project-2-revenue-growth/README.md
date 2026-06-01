# Project 2: Revenue & Growth Analytics
### Olist Brazilian E-Commerce: Commercial Performance & Market Opportunity

**"Where Is the Revenue and Where Should It Go?"**

Most e-commerce dashboards show you total revenue over time and call it a day. This project asks something harder: what's driving performance, where is customer satisfaction breaking down, and which markets are being left on the table?

Using 100K+ real transactions from Olist, Brazil's largest online marketplace (similar to Amazon in the US), paired with [IBGE state-level economic data](https://ibge.gov.br) (Brazilian Institute of Geography and Statistics, 2017), this analysis moves from performance measurement to strategic opportunity sizing across two dashboard pages.

[View Live Dashboard](https://public.tableau.com/app/profile/olivia.watson4893/viz/OlistCommercialGrowthAnalytics_OliviaWatson/Dashboard1) · [View Analysis Code](project-2-revenue-growth/Analysis/scripts/)

Dashboard 1 is live. Dashboard 2 coming soon! :)

---

## What I Built

### Page 1: Commercial Performance

A senior leadership view of the core business: revenue trends, category performance, fulfillment reliability, and customer satisfaction patterns.

**Key findings:**
- GMV grew from ~$300K/month in early 2017 to ~$1M/month by November 2017, driven by a clear holiday season spike
- Health & Beauty and Watches & Gifts lead revenue, together accounting for nearly $2.4M, or 18% of total GMV
- 91.9% of orders are delivered on time nationally, but MA sits at 76.9%, a significant outlier that correlates with lower review scores
- Review scores are bimodal: 58% are 5-star and 11% are 1-star. The middle is thin. Delivery experience is most likely the dividing factor.

### Page 2: Where to Grow *(coming soon)*

A market opportunity analysis that merges Olist transaction data with Brazilian state-level economic data (IBGE, 2017) to identify where e-commerce revenue is undertapped relative to regional wealth and population. The merge is what makes this analysis meaningful: benchmarking performance against national economic data lets you see underpenetration, not just low revenue.

Planned analysis includes:
- Regional opportunity matrix: GMV per capita vs. GDP per capita by state
- Repeat purchase rate by state: a retention proxy across the customer base
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

- **Transaction data:** [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Kaggle, 9 CSV files, 100K+ orders (2016-2018)
- **State economic data:** [IBGE Regional Accounts of Brazil, 2017](https://ibge.gov.br). Brazilian Institute of Geography and Statistics. Values compiled from published tables.

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

## Assumptions

- **Delivered orders only.** All revenue, satisfaction, and delivery metrics are filtered to orders with status = "delivered." Canceled, unavailable, and in-progress orders are excluded. This is the right scope for a commercial performance analysis: we're measuring what actually reached the customer. Future analysis could look further at cancellations, availability, and time to fulfillment.

- **On-time delivery is defined by the platform's own estimate.** On-time means `order_delivered_customer_date <= order_estimated_delivery_date`. This measures whether Olist met its own promise to the customer, not whether the delivery was fast in absolute terms. A seller could have a 100% on-time rate and still take 3 weeks to deliver.

- **Repeat purchase rate (3%) reflects the platform model, not a data problem.** Olist is a discovery marketplace where most buyers arrive via search for a specific product. Low repeat rates are a structural characteristic of this model, not a signal that something is wrong with the data or the business.

- **State economic data is from 2017.** IBGE publishes regional accounts annually. 2017 was chosen because it represents the peak transaction period in the dataset. Using 2016 or 2018 figures would not materially change the opportunity matrix findings.

- **GMV per capita uses customer state, not seller state.** The regional opportunity analysis reflects where buyers are located, not where sellers ship from. This is intentional: the question being asked is about demand concentration, not fulfillment geography.

---

## Limitations

- **2016 is a partial year.** The dataset starts in September 2016. Only 2017 is a complete calendar year and serves as the primary baseline. 2018 data ends in October. Year-over-year comparisons need to account for this.

- **No customer demographics.** Age, gender, income, and device type are not available. Almost every finding here would be more actionable with basic demographics, particularly the regional opportunity analysis, where household income at the individual level would sharpen the market sizing significantly.

- **Seller state does not equal origin of goods.** Seller state reflects where the seller is registered, not necessarily where the product ships from or is warehoused. The delivery performance analysis by seller state should be read as a directional signal, not a precise operations metric.

- **The economic data merge is at the state level.** Brazil has 27 states. The opportunity matrix shows state-level patterns, not city or metro-level ones. Sao Paulo state contains both the hyper-dense capital and rural areas: the state average masks significant internal variation.

- **Cohort LTV is a revenue proxy, not true LTV.** True lifetime value requires a churn model and margin data. What is calculated here is cumulative revenue per customer by acquisition cohort, a useful directional signal but not a complete LTV model.

---

## What I Would Do With Better Data

- **Add margin data.** GMV tells you how much customers spent. Contribution margin tells you how much the business kept. A revenue analysis without margin data cannot answer the most important commercial question: which categories, sellers, and regions are actually profitable?

- **Build a proper churn and retention model.** With a subscription or loyalty signal, the repeat purchase analysis could move from a descriptive rate to a predictive model. Which customers are likely to buy again? What triggered the second purchase for the 3% who did?

- **Drill the regional opportunity matrix to city level.** The state-level scatter plot identifies which states are underserved. City-level data, available in the Olist dataset through zip code, would let you identify specific metro areas to prioritize for seller recruitment or marketing investment.

- **Segment seller performance beyond state.** The delivery analysis shows which states have fulfillment problems. The more actionable cut is by individual seller, identifying the specific sellers driving MA's 76.9% on-time rate and understanding whether it is a volume problem, a geography problem, or an operational one.

- **Connect delivery performance to customer lifetime value.** The fulfillment vs. satisfaction scatter suggests that slower delivery drives lower review scores. The next question is whether lower review scores drive lower repurchase. Linking these three metrics would turn a correlation into a causal chain worth acting on.

---

*Last updated: May 2026*
