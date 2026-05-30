# Project 1: Tableau Dashboard Build Spec
### "What Your Weekly Recap Is Missing"
**Olivia Watson | Data Analytics Portfolio**

---

## Overview

**Dashboard concept:** A simulated "Weekly Health Recap" — what a smart wearable app should show its users, built in Tableau Public.

**Audience:** Health tech recruiters and product/analytics teams. Design for the analyst; it will impress the recruiter.

**Data sources (all CSVs from `Analysis/outputs/`):**
- `out_activity_summary.csv` — primary source (1 row per user)
- `out_sleep_efficiency.csv` — join to activity on `user_id`
- `out_consistency.csv` — join to activity on `user_id`
- `out_hourly_patterns.csv` — standalone, no join
- `out_cdc_benchmarks.csv` — reference values for annotations

---

## Design System

**Color palette — Modern Sage (dark theme):**

| Role | Color | Hex |
|------|-------|-----|
| Background | Soft Charcoal | `#1C1C27` |
| Card / container | Deep Navy-Slate | `#252535` |
| Border / divider | Muted Slate | `#3A3A50` |
| Primary data | Sage Green | `#7DAA92` |
| Secondary data | Warm Sand | `#C9B89A` |
| Alert / negative | Terracotta | `#D4856A` |
| Text — headlines | Off-White | `#F0EDE8` |
| Text — labels | Warm Gray | `#9A9AB0` |

**Typography:**
- Font: DM Sans (free, Google Fonts — import via Tableau or use as system font)
- KPI numbers: Bold, 28–36px
- Chart titles: Bold, 16–18px
- Axis labels / annotations: Regular, 11–13px

**Gridlines:** Lighter than the data marks. Use `#3A3A50` at 50% opacity or remove entirely.

**Borders:** None on individual charts. Use background color contrast to separate sections.

---

## Dashboard Layout

```
+----------------------------------------------------------+
|  HEADER: Title + subtitle                                |
+----------------------------------------------------------+
| [KPI 1]    | [KPI 2]    | [KPI 3]    | [KPI 4]          |
| Avg Steps  | Sedentary  | Sleep Eff% | % Meet CDC       |
+----------------------------------------------------------+
|                                                          |
|         HERO CHART: Steps vs. Sedentary Scatter          |
|                   (full width)                           |
|                                                          |
+----------------------------+-----------------------------+
| Sleep Efficiency Bar Chart | Hourly Step Pattern Line   |
|                            |                            |
+----------------------------+-----------------------------+
|       Consistency Dot Plot (full width)                  |
+----------------------------------------------------------+
```

**Layout rules:**
- KPI tiles: top row, equal width, ~180px tall
- Hero chart: 100% width, ~350px tall — this gets the most space
- Second row: 50/50 split
- Consistency chart: full width at bottom, ~250px tall
- Minimum 16px padding between all elements
- No chart should touch the dashboard edge — use consistent outer padding

---

## Chart 1: KPI Tiles (4 tiles across top)

**KPI 1 — Average Daily Steps**
- Value: cohort average from `out_activity_summary.csv`
- Delta: vs. national average of 4,774 (from `out_cdc_benchmarks.csv`)
- Format: show delta as "+X,XXX vs. national avg"
- Color: Sage `#7DAA92` (cohort is above average — positive)

**KPI 2 — Average Sedentary Hours**
- Value: cohort average sedentary hours from `out_activity_summary.csv`
- Delta: vs. national average of 6.5 hours
- Format: show delta as "+X.X hrs vs. national avg"
- Color: Terracotta `#D4856A` (cohort sits MORE than average — flag this)
- Note: sedentary hours include sleep in this dataset — add a small footnote label

**KPI 3 — Average Sleep Efficiency**
- Value: average `avg_sleep_efficiency_pct` from `out_sleep_efficiency.csv`
- Filter: users with `sleep_days_recorded >= 5` only
- Format: XX.X%
- Color: Sage if above 85%, Terracotta if below
- Sub-label: "Clinical threshold: 85%"

**KPI 4 — % Meeting CDC Activity Guideline**
- Value: count of users where `cdc_activity_status = 'Meets guideline'` / 33
- Format: XX% (X of 33 users)
- Color: Sage if > 50%, Terracotta if below
- Sub-label: "150 min/week moderate activity"

---

## Chart 2: Hero — Steps vs. Sedentary Scatter (INSIGHT 1)

**Chart type:** Scatter plot

**Data source:** `out_activity_summary.csv`

**Axes:**
- X: `avg_daily_steps` — label "Avg Daily Steps"
- Y: `avg_sedentary_hours` — label "Avg Sedentary Hours/Day"
- X axis range: 0 to 18,000
- Y axis range: 10 to 24

**Marks:**
- Shape: Circle
- Size: Fixed (medium — not too small to click)
- Color: `cdc_activity_status`
  - "Meets guideline" → Sage `#7DAA92`
  - "Below guideline" → Terracotta `#D4856A`
- Tooltip: user_id, avg_daily_steps, avg_sedentary_hours, cdc_activity_status

**Reference lines:**
- Vertical line at X = 4,774 — label "National avg steps"
- Horizontal line at Y = 6.5 — label "National avg sedentary"
- Both lines: dashed, `#9A9AB0`, thin

**Annotation (text box, upper right quadrant):**
- "High steps. High sitting. The paradox."
- Font: DM Sans italic, `#9A9AB0`, 12px

**Title:** "More Steps Doesn't Mean Less Sitting"
**Subtitle:** "Users who hit step goals still accumulate 11–21 sedentary hours per day"

---

## Chart 3: Sleep Efficiency Bar (INSIGHT 2)

**Chart type:** Horizontal bar chart

**Data source:** `out_sleep_efficiency.csv`

**Filter:** `sleep_days_recorded >= 5` (removes users with incomplete data)

**Axes:**
- Y: `user_id` — sorted descending by `avg_sleep_efficiency_pct`
- X: `avg_sleep_efficiency_pct` — label "Sleep Efficiency %"
- X axis range: 60% to 100%

**Marks:**
- Color: stepped diverging palette
  - Below 85%: Terracotta `#D4856A`
  - 85%–92%: Sand `#C9B89A`
  - Above 92%: Sage `#7DAA92`
- Tooltip: user_id, avg_hours_asleep, avg_hours_in_bed, avg_sleep_efficiency_pct, cdc_sleep_status

**Reference line:**
- Vertical line at X = 85% — label "Clinical threshold (85%)"
- Line: dashed, `#F0EDE8`, thin

**Annotation:**
- "2 users fall below the clinical threshold for healthy sleep"
- Place near the low-efficiency bars

**Title:** "Sleep Efficiency: Not Just Hours — Quality"
**Subtitle:** "% of time in bed actually spent asleep"

---

## Chart 4: Hourly Step Pattern Line (TIME OF DAY)

**Chart type:** Line chart

**Data source:** `out_hourly_patterns.csv`

**Axes:**
- X: `hour_of_day` (0–23)
  - Format as: 12am, 3am, 6am, 9am, 12pm, 3pm, 6pm, 9pm
- Y: `avg_steps` — label "Avg Steps"

**Marks:**
- Line color: Sage `#7DAA92`
- Line weight: 2.5px
- No individual point markers (clean line only)
- Area fill below line: Sage at 15% opacity (subtle)

**Annotations (text boxes):**
- At hour 12–14: "Midday peak"
- At hour 18: "Evening peak — highest of the day (avg 599 steps)"
- Font: `#9A9AB0`, 11px

**Title:** "When This Cohort Moves"
**Subtitle:** "Average steps by hour — all 33 users"

---

## Chart 5: Consistency Dot Plot (INSIGHT 3)

**Chart type:** Strip plot / dot plot (Tableau: use circle marks on a single axis)

**Data source:** `out_consistency.csv`

**Axes:**
- X: `avg_daily_steps`
- Y: fixed (all dots on one horizontal band — use a calculated field or constant)
- Or: use `consistency_band` on rows to create 3 horizontal bands (preferred)

**Preferred layout — 3 rows:**
- Row 1: Consistent (CV < 50%)
- Row 2: Moderate (CV 50–80%)
- Row 3: Inconsistent (CV > 80%)
- Each row is a horizontal strip of dots positioned by avg_daily_steps

**Marks:**
- Shape: Circle
- Size: Medium-large
- Color by `consistency_band`:
  - Consistent → Sage `#7DAA92`
  - Moderate → Sand `#C9B89A`
  - Inconsistent → Terracotta `#D4856A`
- Tooltip: user_id, avg_daily_steps, step_cv_pct, min_daily_steps, max_daily_steps, consistency_band

**Annotation:**
- "Same average steps — completely different patterns"
- Point to two users with similar avg_daily_steps but different consistency bands

**Title:** "Consistency Matters More Than Peak Days"
**Subtitle:** "Users grouped by day-to-day step variability (coefficient of variation)"

---

## Filters

**Add to dashboard (apply to scatter + consistency charts):**
- `consistency_band` — multiselect button filter
  - Options: All / Consistent / Moderate / Inconsistent
  - Style: single-value button (cleaner than dropdown)

**Do not filter:**
- Hourly patterns chart (cohort average, not per-user)
- KPI tiles (always show full cohort)

---

## Dashboard Header

**Title (large, bold, `#F0EDE8`):**
What Your Weekly Recap Is Missing

**Subtitle (`#9A9AB0`, regular weight):**
An analysis of 33 Fitbit users — and what the data reveals beyond step counts

**Right-aligned metadata (small, `#9A9AB0`):**
Data: Fitbit (Kaggle) + CDC NHANES 2021–2023 | Olivia Watson | May 2026

---

## Build Order in Tableau

Build in this order — each chart is simpler than the last once you have the data sources connected:

1. Connect all 5 CSV data sources
2. Build KPI tiles first (fastest, confirms data is reading correctly)
3. Build hero scatter (most important chart — get this right before moving on)
4. Build sleep efficiency bar
5. Build hourly line chart
6. Build consistency dot plot
7. Assemble dashboard — place charts, set padding, add title/subtitle
8. Add filters and reference lines
9. Add annotations (text boxes)
10. Final color and font pass — make sure all backgrounds are `#1C1C27`
11. Publish to Tableau Public

---

## Common Tableau Gotchas

**Dark background:** Set dashboard background color to `#1C1C27` first, before placing any charts. Each individual sheet also needs its background set to match — it won't inherit from the dashboard automatically.

**CSV joins:** Connect `out_activity_summary.csv` as your primary source. Add `out_sleep_efficiency.csv` and `out_consistency.csv` as relationships joined on `user_id`. Keep `out_hourly_patterns.csv` as a separate data source — don't try to join it to the user-level data.

**Font:** DM Sans is not a default Tableau font. Either install it as a system font on your Mac before opening Tableau, or use Tableau Book as a fallback. Download DM Sans free from Google Fonts.

**Reference lines:** Right-click on the axis → Add Reference Line → Constant → enter the value. Format as dashed, change color to `#9A9AB0`.

**Annotations:** Use floating text boxes on the dashboard (not on the sheet). This gives you more control over placement.

---

*Last updated: May 2026 | Use alongside project1_process_methodology.md*
