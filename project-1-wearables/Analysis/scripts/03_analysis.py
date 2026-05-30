# ============================================================
# Project 1 — Wearable Health Analytics
# Script 03: Core Analysis
#
# What this does:
#   Runs all SQL queries that produce the analytical outputs
#   for the dashboard. Each section maps to one insight.
#
#   Section 1: User summary — steps, sedentary time, active minutes
#   Section 2: Sleep efficiency — time in bed vs. asleep
#   Section 3: Consistency score — step variance by user
#   Section 4: NHANES benchmark comparison
#   Section 5: Hourly step patterns (time of day)
#
#   All outputs are written to Analysis/outputs/ as CSVs
#   for direct use in Tableau.
# ============================================================

import duckdb
import pandas as pd

OUTPUTS = "/Users/oliviawatson/Desktop/Cowork/Project 1/Analysis/outputs"

con = duckdb.connect()

# ============================================================
# SECTION 1: Daily Activity Summary
# One row per user. Average steps, sedentary minutes, and
# active minutes across all days they recorded.
# Key finding: users can hit step goals AND still be sedentary.
# ============================================================
print("Running Section 1: Activity summary...")

activity_summary = con.execute(f"""
    SELECT
        Id                                          AS user_id,
        COUNT(*)                                    AS days_recorded,
        ROUND(AVG(TotalSteps), 0)                   AS avg_daily_steps,
        ROUND(AVG(SedentaryMinutes), 0)             AS avg_sedentary_minutes,
        ROUND(AVG(SedentaryMinutes) / 60.0, 1)      AS avg_sedentary_hours,
        ROUND(AVG(VeryActiveMinutes), 0)            AS avg_very_active_minutes,
        ROUND(AVG(FairlyActiveMinutes), 0)          AS avg_fairly_active_minutes,
        ROUND(AVG(LightlyActiveMinutes), 0)         AS avg_lightly_active_minutes,
        -- Moderate+ minutes per week (CDC guideline is 150/week)
        ROUND(AVG(VeryActiveMinutes + FairlyActiveMinutes) * 7, 0)
                                                    AS est_weekly_moderate_minutes,
        -- Flag: does this user meet CDC 150 min/week guideline?
        CASE
            WHEN AVG(VeryActiveMinutes + FairlyActiveMinutes) * 7 >= 150
            THEN 'Meets guideline'
            ELSE 'Below guideline'
        END                                         AS cdc_activity_status
    FROM read_csv_auto('{OUTPUTS}/fitbit_daily_activity.csv')
    GROUP BY Id
    ORDER BY avg_daily_steps DESC
""").df()

activity_summary.to_csv(f"{OUTPUTS}/out_activity_summary.csv", index=False)
print(f"  {len(activity_summary)} users | saved to out_activity_summary.csv")
print(activity_summary[['user_id','avg_daily_steps','avg_sedentary_hours','cdc_activity_status']].to_string(index=False))


# ============================================================
# SECTION 2: Sleep Efficiency
# Sleep efficiency = minutes asleep / minutes in bed * 100
# Varies significantly by user. More actionable than raw sleep time.
# ============================================================
print("\nRunning Section 2: Sleep efficiency...")

sleep_efficiency = con.execute(f"""
    SELECT
        Id                                                          AS user_id,
        COUNT(*)                                                    AS sleep_days_recorded,
        ROUND(AVG(TotalMinutesAsleep), 0)                           AS avg_minutes_asleep,
        ROUND(AVG(TotalTimeInBed), 0)                               AS avg_minutes_in_bed,
        ROUND(AVG(TotalMinutesAsleep) / 60.0, 1)                    AS avg_hours_asleep,
        ROUND(AVG(TotalTimeInBed) / 60.0, 1)                        AS avg_hours_in_bed,
        -- Sleep efficiency: what % of time in bed are they actually asleep?
        ROUND(AVG(TotalMinutesAsleep) * 100.0 / AVG(TotalTimeInBed), 1)
                                                                    AS avg_sleep_efficiency_pct,
        -- CDC guideline: adults need 7+ hours sleep
        CASE
            WHEN AVG(TotalMinutesAsleep) >= 420 THEN 'Meets 7hr guideline'
            ELSE 'Below 7hr guideline'
        END                                                         AS cdc_sleep_status
    FROM read_csv_auto('{OUTPUTS}/fitbit_sleep.csv')
    GROUP BY Id
    ORDER BY avg_sleep_efficiency_pct DESC
""").df()

sleep_efficiency.to_csv(f"{OUTPUTS}/out_sleep_efficiency.csv", index=False)
print(f"  {len(sleep_efficiency)} users with sleep data | saved to out_sleep_efficiency.csv")
print(sleep_efficiency[['user_id','avg_hours_asleep','avg_hours_in_bed','avg_sleep_efficiency_pct','cdc_sleep_status']].to_string(index=False))


# ============================================================
# SECTION 3: Consistency Score
# Measures how evenly distributed a user's steps are across days.
# Low std deviation = consistent. High = peaks and crashes.
# A user with 7k steps every day beats one with 15k Mon, 1k rest.
# ============================================================
print("\nRunning Section 3: Consistency score...")

consistency = con.execute(f"""
    SELECT
        Id                                          AS user_id,
        ROUND(AVG(TotalSteps), 0)                   AS avg_daily_steps,
        ROUND(STDDEV(TotalSteps), 0)                AS stddev_steps,
        MIN(TotalSteps)                             AS min_daily_steps,
        MAX(TotalSteps)                             AS max_daily_steps,
        -- Coefficient of variation: stddev / mean. Lower = more consistent.
        -- Expressed as %, easier to read.
        ROUND(STDDEV(TotalSteps) * 100.0 / NULLIF(AVG(TotalSteps), 0), 1)
                                                    AS step_cv_pct,
        CASE
            WHEN STDDEV(TotalSteps) * 100.0 / NULLIF(AVG(TotalSteps), 0) < 50
            THEN 'Consistent'
            WHEN STDDEV(TotalSteps) * 100.0 / NULLIF(AVG(TotalSteps), 0) < 80
            THEN 'Moderate'
            ELSE 'Inconsistent'
        END                                         AS consistency_band
    FROM read_csv_auto('{OUTPUTS}/fitbit_daily_activity.csv')
    GROUP BY Id
    ORDER BY step_cv_pct ASC
""").df()

consistency.to_csv(f"{OUTPUTS}/out_consistency.csv", index=False)
print(f"  {len(consistency)} users | saved to out_consistency.csv")
print(consistency[['user_id','avg_daily_steps','step_cv_pct','consistency_band']].to_string(index=False))


# ============================================================
# SECTION 4: NHANES Benchmark — Cohort vs. National Average
# We use NHANES adults 18+ as the national reference population.
# This establishes that wearable users are self-selected and
# already healthier than average — but still have gaps.
# ============================================================
print("\nRunning Section 4: NHANES benchmark...")

# Pull NHANES adults 18+ only (RIDAGEYR >= 18)
# RIAGENDR: 1 = Male, 2 = Female
# RIDRETH3: 1=Mexican American, 2=Other Hispanic, 3=Non-Hispanic White,
#           4=Non-Hispanic Black, 6=Non-Hispanic Asian, 7=Other/Multi
nhanes_summary = con.execute(f"""
    SELECT
        COUNT(*)                                    AS total_adults,
        ROUND(AVG(RIDAGEYR), 1)                     AS avg_age,
        SUM(CASE WHEN RIAGENDR = 1 THEN 1 ELSE 0 END) AS count_male,
        SUM(CASE WHEN RIAGENDR = 2 THEN 1 ELSE 0 END) AS count_female,
        ROUND(AVG(INDFMPIR), 2)                     AS avg_income_poverty_ratio
    FROM read_csv_auto('{OUTPUTS}/DEMO_L.csv')
    WHERE RIDAGEYR >= 18
""").df()

nhanes_summary.to_csv(f"{OUTPUTS}/out_nhanes_summary.csv", index=False)
print(f"  NHANES adult population summary:")
print(nhanes_summary.to_string(index=False))

# Hardcoded CDC published benchmarks for annotation in Tableau
# Sources: CDC Physical Activity Guidelines, CDC Sleep Data, NHANES summary stats
benchmarks = pd.DataFrame([
    {"metric": "pct_meeting_activity_guideline",
     "nhanes_national_value": 24.2,
     "unit": "% of adults meeting 150 min/week",
     "source": "CDC NHANES 2020"},
    {"metric": "pct_insufficient_sleep",
     "nhanes_national_value": 32.8,
     "unit": "% of adults sleeping < 7 hours",
     "source": "CDC Sleep Surveillance 2022"},
    {"metric": "avg_sedentary_hours_per_day",
     "nhanes_national_value": 6.5,
     "unit": "hours/day",
     "source": "CDC NHANES accelerometer data"},
    {"metric": "avg_daily_steps_nat/Users/oliviawatson/Desktop/Cowork/Project 1/Analysis/Scripts/03_analysis.pyional",
     "nhanes_national_value": 4774,
     "unit": "steps/day",
     "source": "NHANES accelerometer, Tudor-Locke et al."},
])
benchmarks.to_csv(f"{OUTPUTS}/out_cdc_benchmarks.csv", index=False)
print(f"\n  CDC benchmarks saved to out_cdc_benchmarks.csv")


# ============================================================
# SECTION 5: Hourly Step Patterns
# Average steps by hour of day across all users.
# Shows when this cohort is most active — morning, lunch, evening.
# ============================================================
print("\nRunning Section 5: Hourly patterns...")

hourly_patterns = con.execute(f"""
    SELECT
        EXTRACT(HOUR FROM CAST(ActivityHour AS TIMESTAMP))  AS hour_of_day,
        ROUND(AVG(StepTotal), 0)                            AS avg_steps,
        ROUND(MAX(StepTotal), 0)                            AS max_steps,
        COUNT(DISTINCT Id)                                  AS users_recorded
    FROM read_csv_auto('{OUTPUTS}/fitbit_hourly_steps.csv')
    GROUP BY hour_of_day
    ORDER BY hour_of_day
""").df()

hourly_patterns.to_csv(f"{OUTPUTS}/out_hourly_patterns.csv", index=False)
print(f"  24 hours of pattern data | saved to out_hourly_patterns.csv")
print(hourly_patterns.to_string(index=False))

con.close()
print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("6 output files written to Analysis/outputs/")
print("="*60)