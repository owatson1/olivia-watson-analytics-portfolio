-- ============================================================
-- Project 1: Wearable Health Analytics
-- "What Your Weekly Recap Is Missing"
-- Olivia Watson | Data Analytics Portfolio
--
-- Tool: DuckDB (used because it reads CSVs directly aka no import step needed)
-- Data sources:
--   fitbit_daily_activity.csv  — 940 rows, 33 users, ~30 days
--   fitbit_sleep.csv           — 413 rows, 24 users with sleep data
--   fitbit_hourly_steps.csv    — 22,099 rows of hourly step counts
--   DEMO_L.csv                 — 11,933 NHANES adults (2021-2023)
--
-- Analytical question:
--   What behavioral patterns in wearable user data suggest
--   opportunities for personalized health interventions —
--   and what insights would be most actionable for users to
--   see in their app?
--
-- Structure:
--   Query 1 — Activity & sedentary summary by user
--   Query 2 — Sleep efficiency by user
--   Query 3 — Step consistency score by user
--   Query 4 — NHANES national benchmark summary
--   Query 5 — Hourly step patterns (time of day)
-- ============================================================


-- ============================================================
-- QUERY 1: Activity & Sedentary Summary
-- ============================================================
-- What it does:
--   Aggregates daily activity data to one row per user.
--   Calculates average steps, sedentary hours, and active
--   minutes. Flags whether each user meets the CDC guideline
--   of 150 minutes of moderate activity per week.
--
-- Key finding (Insight 1: The Activity-Sedentary Paradox):
--   Users who hit daily step goals still accumulate 11–21
--   hours of sedentary time per day. Steps and sedentary
--   time are not inversely correlated the way most people
--   assume.
--
-- CDC guideline reference:
--   150 min/week of moderate-intensity activity
--   Source: CDC Physical Activity Guidelines for Americans
-- ============================================================

SELECT
    Id                                              AS user_id,

    -- How many days did this user record data?
    COUNT(*)                                        AS days_recorded,

    -- Core activity metrics (averaged across all recorded days)
    ROUND(AVG(TotalSteps), 0)                       AS avg_daily_steps,
    ROUND(AVG(SedentaryMinutes), 0)                 AS avg_sedentary_minutes,
    ROUND(AVG(SedentaryMinutes) / 60.0, 1)          AS avg_sedentary_hours,
    ROUND(AVG(VeryActiveMinutes), 0)                AS avg_very_active_minutes,
    ROUND(AVG(FairlyActiveMinutes), 0)              AS avg_fairly_active_minutes,
    ROUND(AVG(LightlyActiveMinutes), 0)             AS avg_lightly_active_minutes,

    -- Estimated weekly moderate+ activity minutes
    -- (VeryActive + FairlyActive per day × 7)
    -- Used to assess against CDC 150 min/week guideline
    ROUND(AVG(VeryActiveMinutes + FairlyActiveMinutes) * 7, 0)
                                                    AS est_weekly_moderate_minutes,

    -- CDC guideline flag
    CASE
        WHEN AVG(VeryActiveMinutes + FairlyActiveMinutes) * 7 >= 150
        THEN 'Meets guideline'
        ELSE 'Below guideline'
    END                                             AS cdc_activity_status

FROM read_csv_auto('outputs/fitbit_daily_activity.csv')
GROUP BY Id
ORDER BY avg_daily_steps DESC;


-- ============================================================
-- QUERY 2: Sleep Efficiency
-- ============================================================
-- What it does:
--   Calculates average sleep efficiency per user, aka the ratio
--   of time actually asleep to total time spent in bed.
--   This is a more actionable metric than raw sleep duration
--   because it captures sleep quality, not just quantity.
--
-- Key finding (Insight 2: Sleep Efficiency):
--   Sleep efficiency ranges from 64% to 98.5% across users.
--   Two users fall well below the clinical threshold of 85%,
--   suggesting poor sleep quality despite adequate time in bed.
--
-- Clinical reference:
--   85% efficiency is the standard clinical threshold for
--   healthy sleep (American Academy of Sleep Medicine)
--
-- Note on data quality:
--   Only 24 of 33 users have sleep records. Several users
--   show very low average hours asleep (<2 hrs). FLAG: these are
--   likely incomplete recording days, not actual sleep values.
--   Will filter out in Tableau to users with 5+ sleep days recorded.
-- ============================================================

SELECT
    Id                                                              AS user_id,

    -- How many days did this user record sleep data?
    COUNT(*)                                                        AS sleep_days_recorded,

    -- Raw sleep metrics
    ROUND(AVG(TotalMinutesAsleep), 0)                               AS avg_minutes_asleep,
    ROUND(AVG(TotalTimeInBed), 0)                                   AS avg_minutes_in_bed,
    ROUND(AVG(TotalMinutesAsleep) / 60.0, 1)                        AS avg_hours_asleep,
    ROUND(AVG(TotalTimeInBed) / 60.0, 1)                            AS avg_hours_in_bed,

    -- Sleep efficiency: what % of time in bed is the user actually asleep?
    -- Formula: (avg minutes asleep / avg minutes in bed) × 100
    ROUND(AVG(TotalMinutesAsleep) * 100.0 / AVG(TotalTimeInBed), 1)
                                                                    AS avg_sleep_efficiency_pct,

    -- CDC guideline flag: 7+ hours of sleep per night for adults
    CASE
        WHEN AVG(TotalMinutesAsleep) >= 420 THEN 'Meets 7hr guideline'
        ELSE 'Below 7hr guideline'
    END                                                             AS cdc_sleep_status

FROM read_csv_auto('outputs/fitbit_sleep.csv')
GROUP BY Id
ORDER BY avg_sleep_efficiency_pct DESC;


-- ============================================================
-- QUERY 3: Step Consistency Score
-- ============================================================
-- What it does:
--   Measures how evenly distributed a user's steps are across
--   all recorded days using the coefficient of variation (CV).
--   CV = standard deviation / mean, expressed as a percentage.
--   Lower CV = more consistent day-to-day activity pattern.
--
-- Key finding (Insight 3: Consistency Over Intensity):
--   6 of 33 users are classified as "Inconsistent" (CV > 100%),
--   meaning their step counts vary wildly day to day — high
--   peaks offset by very low days. A user with 7,000 steps
--   every day outperforms one with 15,000 steps twice a week
--   and near-zero the rest of the time.
--
-- Consistency bands (defined):
--   Consistent   — CV < 50%   (21 users)
--   Moderate     — CV 50-80%  (6 users)
--   Inconsistent — CV > 80%   (6 users)
-- ============================================================

SELECT
    Id                                              AS user_id,

    -- Average and spread of daily steps
    ROUND(AVG(TotalSteps), 0)                       AS avg_daily_steps,
    ROUND(STDDEV(TotalSteps), 0)                    AS stddev_steps,
    MIN(TotalSteps)                                 AS min_daily_steps,
    MAX(TotalSteps)                                 AS max_daily_steps,

    -- Coefficient of variation (CV): lower = more consistent
    -- NULLIF prevents divide-by-zero for users with 0 avg steps
    ROUND(STDDEV(TotalSteps) * 100.0 / NULLIF(AVG(TotalSteps), 0), 1)
                                                    AS step_cv_pct,

    -- Consistency classification
    CASE
        WHEN STDDEV(TotalSteps) * 100.0 / NULLIF(AVG(TotalSteps), 0) < 50
        THEN 'Consistent'
        WHEN STDDEV(TotalSteps) * 100.0 / NULLIF(AVG(TotalSteps), 0) < 80
        THEN 'Moderate'
        ELSE 'Inconsistent'
    END                                             AS consistency_band

FROM read_csv_auto('outputs/fitbit_daily_activity.csv')
GROUP BY Id
ORDER BY step_cv_pct ASC;


-- ============================================================
-- QUERY 4: NHANES National Benchmark Summary
-- ============================================================
-- What it does:
--   Pulls summary statistics from the NHANES 2021-2023
--   demographics file to characterize the national adult
--   population. Context to show that wearable users
--   are a self-selected, already-healthier population, 
--   which makes the gaps identified in Queries 1-3 more
--   meaningful.
--
-- NHANES column reference:
--   RIDAGEYR  — Age in years
--   RIAGENDR  — Gender (1=Male, 2=Female)
--   RIDRETH3  — Race/ethnicity
--   INDFMPIR  — Income-to-poverty ratio (higher = higher income)
--
-- Note on usage:
--   NHANES is not joined to the Fitbit data. There is no
--   shared key between the two datasets. NHANES is used
--   purely as a published national reference benchmark
--   same way CDC summary statistics are cited in
--   academic / industry research.
-- ============================================================

SELECT
    COUNT(*)                                        AS total_adults,
    ROUND(AVG(RIDAGEYR), 1)                         AS avg_age,
    SUM(CASE WHEN RIAGENDR = 1 THEN 1 ELSE 0 END)  AS count_male,
    SUM(CASE WHEN RIAGENDR = 2 THEN 1 ELSE 0 END)  AS count_female,
    ROUND(AVG(INDFMPIR), 2)                         AS avg_income_poverty_ratio

FROM read_csv_auto('outputs/DEMO_L.csv')
WHERE RIDAGEYR >= 18;  -- Adults only


-- ============================================================
-- QUERY 5: Hourly Step Patterns
-- ============================================================
-- What it does:
--   Aggregates hourly step data across all users to show
--   when the cohort is most active during the day.
--   Reveals two distinct activity peaks: midday & evening.
--   This pattern has implications for wearable app nudge
--   timing — interventions are most effective just before
--   a user's natural activity window.
--
-- Key finding:
--   Peak activity hours are 12pm-2pm and 5pm-7pm.
--   Activity drops sharply after 8pm and is minimal before 6am.
--   Evening peak (6pm, avg 599 steps) is highest part of the day.
-- ============================================================

SELECT
    EXTRACT(HOUR FROM CAST(ActivityHour AS TIMESTAMP))  AS hour_of_day,
    ROUND(AVG(StepTotal), 0)                            AS avg_steps,
    ROUND(MAX(StepTotal), 0)                            AS max_steps,
    COUNT(DISTINCT Id)                                  AS users_recorded

FROM read_csv_auto('outputs/fitbit_hourly_steps.csv')
GROUP BY hour_of_day
ORDER BY hour_of_day;
