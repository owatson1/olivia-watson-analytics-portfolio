# Olivia Watson: Data Analytics Portfolio

Analytics and insights professional with 7+ years of experience translating ambiguous business problems into the right questions, building measurement frameworks, and telling the data story clearly.

**Core tools:** SQL, Tableau, Python, DuckDB, Alteryx, Power BI, Excel (Power Query, VBA)

---

## Projects

### Project 1: Wearable Health Analytics
**"What Your Weekly Recap Is Missing"**

Most wearable apps tell you how many steps you took. This project asks a harder question: what does your data actually reveal about your health behaviors, and what should your app be telling you that it isn't?

Using a real-world [Fitbit dataset](https://www.kaggle.com/datasets/arashnic/fitbit) (33 users, ~30 days) paired with [CDC/NHANES national benchmarks](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Demographics&Cycle=2021-2023), this analysis identifies three behavioral patterns that step counts alone don't capture.

**Tools:** DuckDB, SQL, Python, Tableau Public

**Key findings:**
- Users who hit daily step goals still sit 11-21 hours per day. Steps and sedentary time are independent metrics.
- Sleep efficiency (% of time in bed actually asleep) varies from 64% to 98.5% across users and is more actionable than sleep duration alone
- 6 of 33 users show step variability above 100% CV. Consistency predicts outcomes better than peak activity days.

[View Live Dashboard](https://public.tableau.com/app/profile/olivia.watson4893/viz/WearableHealthAnalytics_OliviaWatson/WeeklyHealthRecap) · [View Analysis Code](project-1-wearables/Analysis/scripts/)

---

### Assumptions

- **NHANES as a benchmark, not a join.** There is no shared identifier between the Fitbit and NHANES datasets. NHANES is used as a published national reference population, the same way CDC summary statistics are cited in research. It tells us where the average American adult sits. It does not tell us anything about these 33 specific users.

- **Sedentary minutes include sleep.** The Fitbit dataset records sedentary minutes as any time the device detects no movement, which includes sleep. The high sedentary averages (11-22 hrs/day) reflect this. A more precise analysis would subtract sleep duration from sedentary time to isolate true waking sedentary behavior.

- **Sleep efficiency is a proxy for sleep quality, not a perfect measure of it.** Sleep efficiency (% of time in bed actually asleep) is a standard clinical metric, but it doesn't capture sleep stages, REM duration, disruptions, or subjective sleep quality. A user with 92% efficiency isn't necessarily sleeping well. This metric is useful but shouldn't be treated as definitive.

- **Consistency bands are judgment calls.** The CV thresholds used to classify users as Consistent (CV < 50%), Moderate (50-80%), or Inconsistent (>80%) are my analytical judgment, not published standards. Different thresholds would produce different groupings. The direction of the finding holds regardless of where the lines are drawn.

- **The CDC 150 min/week guideline refers to moderate-intensity aerobic activity.** Brisk walking, cycling, swimming and similar activities. The Fitbit dataset classifies intensity based on device sensors, not validated exercise type. "Fairly active" and "very active" minutes are used as a proxy, which may over or undercount depending on the activity.

---

### Limitations

- **This is not a representative sample.** The cohort averages 7,519 steps per day, significantly above the national average of 4,774. People who wear fitness trackers are self-selected: more health-conscious, more active, and likely younger and higher-income than the general population. These findings shouldn't be generalized to all adults.

- **The sedentary hours finding likely reflects desk workers or students.** Averages of 11-22 sedentary hours per day are high even accounting for sleep. This suggests the cohort may skew toward knowledge workers or students. Worth flagging as a hypothesis, even though the data can't confirm it.

- **No demographic data.** Age, gender, occupation, and location are not available for these 33 users. This is the biggest limitation of the dataset. Almost every finding here would be more actionable with basic demographics. Age and gender alone would allow segmentation by life stage and biological factors that strongly influence sleep and activity patterns.

- **30-day window.** One month of data is enough to identify patterns but not to measure change over time, seasonal variation, or the effect of any intervention. Longitudinal data (6-12 months) would be significantly more valuable.

- **2016 data.** Wearable technology, user behavior, and device accuracy have all changed since then. Findings are directionally useful but may not reflect current wearable users.

- **Small sample size (n=33).** Patterns here are descriptive, not causal. Any claims about what drives better health outcomes would require a larger sample and proper controls.

---

### What I Would Do With Better Data

- **Adjust hourly activity for individual circadian rhythms.** The hourly step chart shows when the cohort moves in absolute clock time (6pm peak). A more interesting cut would normalize by each user's average wake and sleep time, showing activity relative to hours since waking rather than time of day. That shifts the question from "when do people move" to "where in their day do people move most." It also opens up a separate analysis of sleep and wake time distribution across the cohort.

- **Segment by demographics.** With age and gender data, almost every chart in this dashboard gets more actionable. Sleep efficiency by age group. Consistency by gender. Sedentary hours by life stage. These are the cuts a product team would actually use to build personalized interventions.

- **Separate waking sedentary time from sleep.** Subtracting each user's recorded sleep duration from sedentary minutes would give a cleaner picture of how much people actually sit during waking hours. Straightforward calculation with the data available.

- **Test whether consistency predicts other outcomes.** The consistency finding is descriptive right now. The more interesting question: do consistent users show better sleep efficiency, lower sedentary time, or higher active minutes? A correlation analysis across these metrics would turn this into a predictive insight.

- **Add sleep and wake time distribution.** With sleep timestamp data (not just duration), visualizing when users go to bed and wake up would add a meaningful layer. Combined with the hourly activity chart, it would tell a richer story about behavioral clustering and where a wearable app's nudge timing should actually land.

- **Data Sources:**
- [Fitbit Fitness Tracker Data](https://www.kaggle.com/datasets/arashnic/fitbit): Kaggle, 33 users, April-May 2016
- [CDC NHANES 2021-2023 Demographics](https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Demographics&Cycle=2021-2023): National health survey, 11,933 adults

---

### Project 2: Revenue & Growth Analytics

"Where Is the Revenue and Where Should It Go?"
A commercial performance and market opportunity analysis of 100K+ Brazilian e-commerce transactions. Built for a senior commercial or RevOps audience — the kind of analysis you'd bring to a leadership meeting, not just a reporting review.
Page 1 covers core performance fundamentals. Page 2 layers in Brazilian state-level economic data to identify where e-commerce revenue is undertapped relative to regional wealth and population.
Tools: DuckDB · SQL · Python · Tableau Public
Key findings:

GMV grew from ~$300K/month to ~$1M/month over 2017, with a clear holiday season spike in November
Health & Beauty and Watches & Gifts lead revenue at $1.2M each — together 18% of total GMV
91.9% national on-time delivery rate, but MA sits at 76.9% — a meaningful outlier
Review scores are bimodal: 58% are 5-star, 11% are 1-star — delivery experience appears to be the dividing factor

View Live Dashboard · View Analysis Code

*Dashboard 2 of Project 2 coming soon*

### Project 3: Strategic Case Study
*Coming soon*

---

*Last updated: May 2026*
