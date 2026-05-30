# Project 1: Wearable Health Analytics — Process & Methodology
### "What Your Weekly Recap Is Missing"
**Olivia Watson | Data Analytics Portfolio**

---

## What This Document Is

A plain-English walkthrough of every analytical and technical decision made in this project — what I did, why I did it, and what I would say about it in an interview. Written in first person because this is my work and my thinking.

---

## The Starting Point: What Question Am I Actually Answering?

Most wearable analytics projects end at description: here are average steps, here is average sleep. That's not analysis — that's a summary. I wanted to ask a harder question.

The business question I set out to answer:

> *What behavioral patterns in wearable user data suggest opportunities for personalized health interventions — and what insights would be most actionable for users to see in their app?*

The framing matters. I'm not analyzing data for its own sake. I'm thinking like a product analytics team at a health tech company — Oura, Whoop, Fitbit/Google — who needs to decide what to surface in a weekly recap to actually change user behavior. Every analytical choice flows from that framing.

---

## The Data

### Primary: Fitbit Fitness Tracker Data
- **Source:** Kaggle (publicly available, arashnic/fitbit)
- **Users:** 33 unique users
- **Time period:** April–May 2016 (~30 days of data per user)
- **Files used:**
  - `dailyActivity_merged.csv` — steps, active minutes by intensity, sedentary minutes, calories (940 rows)
  - `sleepDay_merged.csv` — total minutes asleep, total time in bed (413 rows, 24 users)
  - `hourlySteps_merged.csv` — step count per hour per user (22,099 rows)
  - `hourlyIntensities_merged.csv` — intensity per hour per user (22,099 rows)

**Why these four files and not the others?**
The dataset contains ~18 files including minute-level granularity, heart rate, and weight logs. I chose daily and hourly files because they match the weekly recap framing — a weekly summary doesn't need minute-level data, and heart rate and weight had too many missing users to be analytically useful.

**Known limitation:** No demographic data. Age, gender, and location are not available for the 33 Fitbit users. I treat this cohort as a proxy for the engaged wearable-wearing population — self-selected and likely already healthier than average.

### Benchmark: CDC / NHANES Demographics (2021–2023)
- **Source:** CDC NHANES public data portal (no approval required)
- **File:** `DEMO_L.xpt` — converted to CSV using Python
- **Adults in dataset:** 8,153 (filtered to age 18+)

**How NHANES is used — and how it isn't:**
NHANES is not joined to the Fitbit data. There is no shared identifier between the two datasets, and attempting a statistical join would be methodologically incorrect. Instead, I use NHANES as a published national reference population — the same way CDC summary statistics are cited in academic and industry research. The NHANES dataset validates that my benchmark figures come from the actual 2021-2023 survey, not a secondary source.

The four CDC benchmarks used as reference points in the dashboard:
- 24.2% of adults meet the 150 min/week physical activity guideline
- 32.8% of adults get insufficient sleep (<7 hours)
- 6.5 average sedentary hours per day nationally
- 4,774 average daily steps nationally (NHANES accelerometer data)

---

## Tool Choices

| Tool | Purpose | Why this tool |
|------|---------|---------------|
| Python (pandas, pyreadstat) | Convert NHANES .xpt to CSV; data validation | Required for .xpt format; pandas for preview and file handling |
| DuckDB | All SQL analysis | Reads CSVs directly without a database setup; near-identical syntax to standard SQL; increasingly used in analytics roles |
| Tableau Public | Dashboard visualization | Free, shareable, portfolio-appropriate; expert-level output possible |
| GitHub | Documentation and code storage | Standard for analytics portfolios; shows version control awareness |

**Why DuckDB over SQLite?**
DuckDB reads CSV files directly without an import step, which keeps the workflow clean and reproducible. It also handles analytical functions (window functions, STDDEV, EXTRACT) more cleanly than SQLite. The syntax is standard SQL — nothing in these queries is DuckDB-specific.

---

## The Three Insights: Analytical Decisions

### Insight 1: The Activity-Sedentary Paradox

**The finding:** Users who average 16,000 steps per day still sit for 18+ hours. Steps and sedentary time are not inversely correlated.

**Why this is analytically interesting:** Most people — and most wearable apps — treat step count as the primary proxy for health. This analysis shows that a user can "win" on steps and still spend the majority of their day sedentary. The two metrics are independent, which means step count alone is insufficient as a health signal.

**How I measured it:** Aggregated `SedentaryMinutes` from the daily activity file to a per-user average, converted to hours. Plotted against average daily steps in a scatter chart. The lack of negative correlation is the finding — if steps and sedentary time were inversely related, the scatter would show a clear downward slope. It doesn't.

**CDC connection:** The 6.5 hours national sedentary average becomes the benchmark line on the chart. The Fitbit cohort averages significantly higher — 11–22 hours sedentary per day depending on the user — which is striking even accounting for sleep being counted as sedentary in this dataset.

**Interview talking point:** "I noticed that the most active users by step count were also among the most sedentary by sitting time. That's counterintuitive, and it's exactly the kind of insight a product team would want to surface — because it changes what the app should tell users."

---

### Insight 2: Sleep Efficiency

**The finding:** Sleep efficiency (minutes asleep ÷ minutes in bed) ranges from 64% to 98.5% across users. It varies more than total sleep time and is more actionable.

**Why this metric and not just sleep duration?**
Total sleep time tells you how long someone slept. Sleep efficiency tells you how well they slept — specifically, whether time in bed is being used for actual sleep. A user who spends 8 hours in bed but only sleeps 6.5 has a different problem than a user who spends exactly 6.5 hours in bed and sleeps all of it. The intervention — and therefore the app message — should be different for each.

**How I measured it:**
```sql
AVG(TotalMinutesAsleep) * 100.0 / AVG(TotalTimeInBed)
```
Averaged at the user level across all recorded sleep days. Clinical threshold for healthy sleep efficiency is 85% (American Academy of Sleep Medicine standard).

**Data quality note:** Three users show average sleep under 2 hours, which is not physiologically plausible as a true average. These are incomplete recording days — the user wore the device in bed some nights but not all. In the dashboard, I filter to users with 5+ sleep days recorded to remove this noise. I document this decision rather than silently dropping rows.

**Interview talking point:** "Sleep efficiency is a standard clinical metric but it's rarely surfaced in consumer wearable apps. The data showed meaningful variation across users — and two users with efficiency below 64% would be told completely different things than users who just need more hours. That's a product insight, not just a data point."

---

### Insight 3: Consistency Over Intensity

**The finding:** 6 of 33 users have a step coefficient of variation above 100%, meaning their daily steps vary more than their average — high peaks offset by near-zero days.

**The metric — coefficient of variation (CV):**
CV = (standard deviation / mean) × 100

This is a standard statistical measure of relative variability. I chose it over standard deviation alone because it's normalized — a CV of 50% means the same thing whether a user averages 3,000 steps or 15,000 steps. Raw standard deviation doesn't allow fair comparison across users with very different averages.

**Why consistency matters more than peak activity:**
Research consistently shows that moderate, regular physical activity produces better health outcomes than sporadic intense activity. A user averaging 7,000 steps every day accumulates 49,000 steps per week. A user who hits 15,000 steps twice a week and fewer than 1,000 the other five days accumulates roughly 35,000 — and misses the metabolic benefit of regular movement.

**Consistency bands I defined:**
- Consistent: CV < 50% (21 users) — relatively even day-to-day
- Moderate: CV 50–80% (6 users) — some variability
- Inconsistent: CV > 80% (6 users) — high peaks, low valleys

These thresholds are my analytical judgment call, not published standards. I'd document this in any stakeholder-facing work.

**Interview talking point:** "The coefficient of variation is something I use to normalize variability across users with different baselines. It's a more honest metric than standard deviation when you're comparing people who have very different average step counts."

---

## What I Would Do With More Time or Better Data

**Demographics:** The Fitbit dataset has no age, gender, or location data. With demographics, I could segment the consistency and sedentary findings by age group — which would be significantly more actionable for a product team.

**Longitudinal data:** 30 days is enough to identify patterns but not to measure behavior change. A 6-month dataset would allow cohort analysis: do users who receive consistency nudges actually improve over time?

**Heart rate:** The dataset includes heart rate data, but fewer than 15 users have meaningful records. With complete heart rate data, I could calculate actual exercise intensity rather than relying on the device's intensity classification.

**Statistical testing:** The patterns I identify are descriptive. To make causal claims — "inconsistent users are less healthy" — I'd need to run significance tests and control for confounders. That's outside scope for this dataset but worth noting.

---

## File Structure

```
Project 1/
├── Data/                          ← raw source files, never modified
│   ├── DEMO_L.xpt                 ← NHANES 2021-2023 demographics
│   └── FitBit Dataset/            ← original Kaggle download
│       └── archive 2/             ← source data used
└── Analysis/
    ├── scripts/
    │   ├── 01_setup_nhanes.py     ← converts DEMO_L.xpt to CSV
    │   ├── 02_validate_data.py    ← copies files, validates row counts
    │   ├── 03_analysis.py         ← runs all queries, writes outputs
    │   └── 04_analysis_queries.sql ← clean SQL for GitHub
    └── outputs/                   ← all files that feed Tableau
        ├── DEMO_L.csv
        ├── fitbit_daily_activity.csv
        ├── fitbit_sleep.csv
        ├── fitbit_hourly_steps.csv
        ├── fitbit_hourly_intensities.csv
        ├── out_activity_summary.csv
        ├── out_sleep_efficiency.csv
        ├── out_consistency.csv
        ├── out_hourly_patterns.csv
        └── out_cdc_benchmarks.csv
```

---

## Interview Quick Reference

**"Walk me through this project."**
I started with a product question — what should a wearable app's weekly recap actually tell users — and worked backward to the data. I used a public Fitbit dataset of 33 users and paired it with NHANES national benchmarks to add population-level context. The three core findings are the activity-sedentary paradox, sleep efficiency variation, and step consistency. Each maps to a feature a health tech company could build.

**"Why DuckDB?"**
It reads CSVs directly without a database setup, handles analytical SQL cleanly, and is increasingly common in analytics roles. The SQL syntax is standard — nothing in this project is DuckDB-specific.

**"Why NHANES?"**
To add context. Without a national benchmark, the Fitbit data just describes 33 people. With it, I can say: this cohort is already more active than 70% of American adults, which makes the gaps I found more interesting, not less — even people who self-select into wearables have room to improve on sedentary time and sleep.

**"What would you do differently?"**
Demographics in the Fitbit data would unlock segmentation by age and gender. Longitudinal data would let me measure actual behavior change. And with heart rate data I could validate the intensity classifications the device uses rather than taking them at face value.

---

*Last updated: May 2026 | Project 1 of 3*
