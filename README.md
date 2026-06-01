# Olivia Watson: Analytics Portfolio

**Senior Analytics Professional | Revenue Operations | Growth Analytics | Health Tech**

[Tableau Public](https://public.tableau.com/app/profile/olivia.watson4893) · [LinkedIn](#) · [Email](#)

---

## About Me

I'm a senior analytics professional with 7+ years of experience turning ambiguous business problems into clear, actionable findings. My background spans federal healthcare programs, operations, and strategy, which means I've spent a lot of time asking hard questions of messy data and explaining the answers in a way that actually drives decisions, not just documents findings.

My core value is the layer between the data and the decision: building the right measurement framework, asking the question nobody thought to ask, and making the findings readibly available to the people who need to act on them.

I'm an expert-level Tableau and Alteryx user, and my SQL placed in the top 10% on TestDome. My Python is solid for analytics work. Across my career I've worked across a wide range of tools, and I think the more important skill is knowing the tradeoffs: choosing the wrong tool at the start creates rework, wasted time, and compounding headaches. I've consistently worked with teams and stakeholders upfront to make the right data decisions before building, not after. For a fuller picture of my tool experience, feel free to check my LinkedIn, request my resume, or reach out directly.

More important to me than any specific tool is the thinking around it: the upfront planning, the data logic, the QA, the inconsistency hunting, the so-what. That's where the real work is, and that's where I live.

On AI: I use it as a tool, not a replacement for thinking. It handles the repetitive and mechanical work well. The planning, the strategic framing, the quality checks, and the judgment calls stay with me.

---

## A Note on These Projects

My entire career has been in environments with highly sensitive data and PHI, which means the work I'm proudest of can't be shared publicly. These projects are personal work, built on public datasets, done out of genuine interest in the problems. In practice, I'm used to working with datasets in the millions of records, complex merges and joins, and large automated dashboarding and reporting systems. These projects scratch the surface of that, but they represent the same thinking I bring to everything: start with a real question, build something that actually answers it, and make it clear enough that someone else can act on it. Always excited to do more.

---

## This Portfolio

Each project has a business question worth asking, analysis built to answer it, a live dashboard, and documentation that explains the decisions along the way.

All work is published to Tableau Public and GitHub. Dashboards are built as scrollable views for portfolio accessibility. In a production or leadership context, these would be reformatted for fixed-dimension presentation or split into separate views. That's a deliberate tradeoff, not an oversight.

---

## Projects

### Project 1: Wearable Health Analytics
**"What Your Weekly Recap Is Missing"**

Most wearable apps tell you how many steps you took. This project asks a harder question: what does your data actually reveal about your health behaviors, and what should your app be telling you that it isn't?

Using a real-world Fitbit dataset (33 users, ~30 days) paired with CDC/NHANES national benchmarks, this analysis identifies three behavioral patterns that step counts alone don't capture.

**Tools:** DuckDB, SQL, Python, Tableau Public  
**Key findings:**
- Users who hit daily step goals still sit 11-21 hours per day; steps and sedentary time are independent metrics
- Sleep efficiency varies from 64% to 98.5% across users and is more actionable than sleep duration alone
- 6 of 33 users show step variability above 100% CV; consistency predicts outcomes better than peak activity days

[View Dashboard](https://public.tableau.com/app/profile/olivia.watson4893/viz/WearableHealthAnalytics_OliviaWatson/WeeklyHealthRecap) · [View Code & Documentation](project-1-wearables/)

---

### Project 2: Revenue & Growth Analytics
**"Where Is the Revenue and Where Should It Go?"**

Most e-commerce dashboards show you total revenue over time and call it a day. This project asks something harder: what's driving performance, where is customer satisfaction breaking down, and which markets are being left on the table?

Using 100K+ real transactions from Olist, Brazil's largest online marketplace, paired with IBGE state-level economic data, this analysis moves from performance measurement to strategic opportunity sizing across two dashboard pages.

**Tools:** DuckDB, SQL, Python, Tableau Public  
**Key findings:**
- A small seller segment drives outsized revenue but shows meaningfully lower satisfaction scores, a retention and quality risk
- Late deliveries correlate directly with satisfaction drops; the gap between estimated and actual delivery dates is the more predictive metric
- Several states with above-average GDP per capita are significantly underpenetrated relative to their economic potential

[View Dashboard](https://public.tableau.com/app/profile/olivia.watson4893/viz/OlistCommercialGrowthAnalytics/CommercialPerformance) · [View Code & Documentation](project-2-revenue-growth/)

---

## How to Navigate This Repo

```
olivia-watson-analytics-portfolio/
│
├── project-1-wearables/
│   ├── README.md                  ← Start here for project context
│   ├── Analysis/
│   │   ├── scripts/               ← SQL and Python files
│   │   └── outputs/               ← CSV exports used in Tableau
│
├── project-2-revenue-growth/
│   ├── README.md                  ← Start here for project context
│   ├── Analysis/
│   │   ├── scripts/               ← SQL and Python files
│   │   └── outputs/               ← CSV exports used in Tableau
│
└── README.md                      ← You are here
```

Each project README covers the business question, data sources, analytical decisions (and why), key findings, and what I'd do with more data or time. The code is commented throughout. The README is where the thinking lives.

---

*Last updated: June 2026*
