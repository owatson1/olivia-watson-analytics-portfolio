# ============================================================
# Project 1 — Wearable Health Analytics
# Script 01: Setup + NHANES Data Conversion
#
# What this does:
#   1. Installs required libraries (duckdb, pandas, pyreadstat)
#   2. Converts DEMO_L.xpt (SAS format) to a CSV file
#   3. Prints a preview so you can verify the data loaded correctly
#
# Run this once. After this, DEMO_L.csv lives in outputs/
# and is ready to query with DuckDB.
# ============================================================

import subprocess
import sys

# --- Install required libraries ---
subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb", "pandas", "pyreadstat"])

import pandas as pd
import pyreadstat
import duckdb

# --- File paths ---
xpt_path = "/Users/oliviawatson/Desktop/Cowork/Project 1/Data/DEMO_L.xpt"
output_path = "/Users/oliviawatson/Desktop/Cowork/Project 1/Analysis/outputs/DEMO_L.csv"

# --- Convert .xpt to CSV ---
print("Converting DEMO_L.xpt to CSV...")
df, meta = pyreadstat.read_xport(xpt_path, encoding="latin1")
df.to_csv(output_path, index=False)
print(f"Done. {len(df)} rows written to DEMO_L.csv")

# --- Quick sanity check ---
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 3 rows:")
print(df.head(3))