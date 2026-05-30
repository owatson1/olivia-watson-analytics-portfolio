# Olivia Watson: Data Analytics Portfolio

Analytics and insights professional with 7+ years of experience translating ambiguous business problems into the right questions, building measurement frameworks, and telling the data story clearly.

**Core tools:** SQL · Tableau · Python · DuckDB · Alteryx · Power BI · Excel (Power Query, VBA)

---

## Projects

### Project 1: Wearable Health Analytics
**"What Your Weekly Recap Is Missing"**

Most wearable apps tell you how many steps you took. This project asks a harder question: what does your data actually reveal about your health behaviors — and what should your app be telling you that it isn't?

Using a real-world Fitbit dataset (33 users, ~30 days) paired with CDC/NHANES national benchmarks, this analysis identifies three behavioral patterns that step counts alone don't capture.

**Tools:** DuckDB · SQL · Python · Tableau Public

**Key findings:**
- Users who hit daily step goals still sit 11–21 hours per day. Steps and sedentary time are independent metrics
- Sleep efficiency (% of time in bed actually asleep) varies from 64% to 98.5% across users and is more actionable than sleep duration alone
- 6 of 33 users show step variability above 100% CV. Consistency predicts outcomes better than peak activity days

[View Live Dashboard](https://public.tableau.com/app/profile/olivia.watson4893/viz/WearableHealthAnalytics_OliviaWatson/WeeklyHealthRecap) · [View Analysis Code](project-1-wearables/Analysis/scripts/)

---

### Assumptions

- **NHANES as a benchmark, not a join.** There is no shared identifier between the Fitbit and NHANES datasets. NHANES is used purely as a published national reference population — the same way CDC summary statistics are cited in research. It tells us where the average American adult sits; it does not tell us anything about these 33 specific users.

- **Sedentary minutes include sleep.** The Fitbit dataset records sedentary minutes as any time the device detects no movement — this includes sleep. The high sedentary averages (11–22 hrs/day) reflect this. A more precise analysis would subtract sleep duration from sedentary time to isolate true waking sedentary behavior.

- **Sleep efficiency as a proxy for sleep quality.** Sleep efficiency (% of time in bed actually asleep) is a standard clinical metric, but it is not a complete measure of sleep quality. It does not capture sleep stages, REM duration, disruptions, or subjective sleep quality. A user with 92% efficiency is not necessarily sleeping well — they may simply be efficient at lying awake before falling asleep. This metric is directionally useful but should not be treated as definitive.

- **Consistency bands are judgment calls.** The coefficient of variation thresholds used to classify users as Consistent (CV < 50%), Moderate (50–80%), or Inconsistent (>80%) are my analytical judgment, not published standards. Different thresholds would produce different groupings. The direction of the finding holds regardless of where exactly the lines are drawn.

- **CDC 150 min/week guideline refers to moderate-intensity aerobic activity.** This includes brisk walking, cycling, swimming, and similar activities. The Fitbit dataset classifies intensity based on device sensors, not validated exercise type. "Fairly active" and "very active" minutes are used as a proxy for moderate-intensity activity — this is a reasonable approximation but may over or undercount depending on the activity.

---

### Limitations

- **This is not a representative sample.** The cohort averages 7,519 steps per day — significantly above the national average of 4,774. People who wear fitness trackers are self-selected: they are more health-conscious, more active, and likely younger and higher-income than the general population. Findings about this cohort should not be generalized to all adults.

- **The sedentary hours finding likely reflects desk workers or students.** Sedentary averages of 11–22 hours per day are high even accounting for sleep. This suggests the cohort may skew toward knowledge workers or students with largely sedentary working hours. Without demographic data we cannot confirm this, but it is a reasonable hypothesis worth flagging.

- **No demographic data.** Age, gender, occupation, and location are not available for these 33 users. This is the single biggest limitation of this dataset. Almost every finding in this analysis would be more actionable with even basic demographics — age and gender alone would allow segmentation by life stage and biological factors that strongly influence sleep and activity patterns.

- **30-day window.** One month of data is enough to identify behavioral patterns but not to measure change over time, seasonal variation, or the effect of any intervention. Longitudinal data (6–12 months) would be significantly more valuable for a product team.

- **2016 data.** The dataset was collected in 2016. Wearable technology, user behavior, and device accuracy have all changed since then. Findings are directionally valid but may not reflect current wearable users.

- **Small sample size (n=33).** Statistical significance is limited. Patterns are descriptive, not causal. Any claims about what "causes" better health outcomes would require a much larger sample and proper controls.

---

### What I Would Do Differently With Better Data

- **Adjust hourly activity for individual circadian rhythms.** The hourly step chart shows when the cohort moves in absolute time (6pm peak). A more interesting analysis would normalize by each user's average wake and sleep time — showing activity relative to hours since waking rather than clock time. This would reveal whether people are most active early in their day, mid-day, or late, regardless of when they wake up. It also opens up analysis of sleep and wake time distribution across the cohort, which could be visualized as a separate chart.

- **Segment by demographics.** With age and gender data, almost every chart in this dashboard becomes more actionable. Sleep efficiency by age group. Consistency scores by gender. Sedentary hours by life stage. These are the cuts a product team would actually use to build personalized interventions.

- **Separate waking sedentary time from sleep.** Recalculating sedentary hours by subtracting each user's recorded sleep duration would produce a more honest picture of how much people actually sit during their waking hours. This is a straightforward calculation with the data available but would require a methodological note.

- **Test whether consistency predicts other outcomes.** The consistency finding is descriptive — I show that some users are more consistent than others. The more interesting question is whether consistent users show better sleep efficiency, lower sedentary time, or higher active minutes. A correlation analysis across these metrics would turn a descriptive observation into a predictive insight.

- **Add sleep and wake time distribution.** If sleep timestamp data were available (not just duration), visualizing the distribution of when users go to bed and wake up would add a meaningful layer. Combined with the hourly activity chart, it would tell a richer story about how behavioral patterns cluster across the cohort — and where a wearable app's nudge timing should actually land.

---

### Project 2: Revenue & Growth Analytics
*Coming soon*

### Project 3: Strategic Case Study
*Coming soon*

---

*Last updated: May 2026*
