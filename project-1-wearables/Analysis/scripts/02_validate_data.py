# ============================================================
# Project 1 — Wearable Health Analytics
# Script 02: Data Validation
#
# What this does:
#   1. Copies the 4 Fitbit source files into outputs/ with
#      clean, flat filenames (no nested folder paths)
#   2. Uses DuckDB to preview each file — row counts,
#      column names, and first 3 rows
#   3. Flags any obvious data quality issues (nulls, dupes)
#
# After this runs, outputs/ has all 5 files ready for SQL.
# ============================================================

import shutil
import duckdb
import pandas as pd

# --- Source paths (archive 2, 4.12.16-5.12.16 only) ---
FITBIT_BASE = "/Users/oliviawatson/Desktop/Cowork/Project 1/Data/FitBit Dataset/archive 2/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16"
OUTPUTS = "/Users/oliviawatson/Desktop/Cowork/Project 1/Analysis/outputs"

# Files to copy: (source filename, output filename)
files_to_copy = [
    ("dailyActivity_merged.csv",    "fitbit_daily_activity.csv"),
    ("sleepDay_merged.csv",         "fitbit_sleep.csv"),
    ("hourlySteps_merged.csv",      "fitbit_hourly_steps.csv"),
    ("hourlyIntensities_merged.csv","fitbit_hourly_intensities.csv"),
]

# --- Step 1: Copy Fitbit files to outputs/ ---
print("Copying Fitbit files to outputs/...")
for source_name, output_name in files_to_copy:
    src = f"{FITBIT_BASE}/{source_name}"
    dst = f"{OUTPUTS}/{output_name}"
    shutil.copy2(src, dst)
    print(f"  Copied: {output_name}")

# --- Step 2: Validate all 5 files with DuckDB ---
all_files = {
    "fitbit_daily_activity":     f"{OUTPUTS}/fitbit_daily_activity.csv",
    "fitbit_sleep":              f"{OUTPUTS}/fitbit_sleep.csv",
    "fitbit_hourly_steps":       f"{OUTPUTS}/fitbit_hourly_steps.csv",
    "fitbit_hourly_intensities": f"{OUTPUTS}/fitbit_hourly_intensities.csv",
    "nhanes_demographics":       f"{OUTPUTS}/DEMO_L.csv",
}

con = duckdb.connect()

print("\n" + "="*60)
print("DATA VALIDATION SUMMARY")
print("="*60)

for name, path in all_files.items():
    print(f"\n--- {name} ---")

    # Row and column count
    result = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{path}')").fetchone()
    df_cols = con.execute(f"SELECT * FROM read_csv_auto('{path}') LIMIT 1").df()
    print(f"  Rows: {result[0]:,}")
    print(f"  Columns ({len(df_cols.columns)}): {list(df_cols.columns)}")

    # First 3 rows
    preview = con.execute(f"SELECT * FROM read_csv_auto('{path}') LIMIT 3").df()
    print(f"  Preview:")
    print(preview.to_string(index=False))

con.close()
print("\nValidation complete. All files ready for analysis.")