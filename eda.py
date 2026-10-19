import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from preprocessing import load_and_clean_data, validate_data
from analysis import create_metrics, identify_high_load_periods


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_PATH = Path(__file__).resolve().parent

DATA_PATH = (
    PROJECT_PATH
    / "data"
    / "HHS_Unaccompanied_Alien_Children_Program.csv"
)

OUTPUT_PATH = PROJECT_PATH / "outputs"
FIGURES_PATH = OUTPUT_PATH / "figures"

OUTPUT_PATH.mkdir(exist_ok=True)
FIGURES_PATH.mkdir(exist_ok=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("\n======================================")
print("UAC SYSTEM CAPACITY ANALYTICS")
print("======================================")

print("\nLoading dataset...")

df = load_and_clean_data(DATA_PATH)

print("Dataset loaded successfully!")

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print(
    "Date range:",
    df["Date"].min(),
    "to",
    df["Date"].max()
)


# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

print("\n======================================")
print("DATA QUALITY")
print("======================================")

checks = validate_data(df)

for key, value in checks.items():
    print(f"{key}: {value}")


# --------------------------------------------------
# CREATE METRICS
# --------------------------------------------------

df = create_metrics(df)

print("\n======================================")
print("PROJECT METRICS CREATED")
print("======================================")

print(
    df[
        [
            "Date",
            "Total System Load",
            "Net Intake Pressure",
            "Load Change Since Previous Report",
            "Discharge Offset Ratio",
            "Cumulative Net Pressure",
        ]
    ].head()
)


# --------------------------------------------------
# STATISTICS
# --------------------------------------------------

print("\n======================================")
print("STATISTICAL SUMMARY")
print("======================================")

print(
    df[
        [
            "Children in CBP custody",
            "Children in HHS Care",
            "Children transferred out of CBP custody",
            "Children discharged from HHS Care",
            "Total System Load",
            "Net Intake Pressure",
        ]
    ].describe()
)


# --------------------------------------------------
# TOTAL SYSTEM LOAD GRAPH
# --------------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    df["Date"],
    df["Total System Load"],
    linewidth=2
)

plt.title(
    "Total UAC System Care Load Over Time"
)

plt.xlabel("Date")

plt.ylabel(
    "Children Under Care"
)

plt.xticks(rotation=45)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    FIGURES_PATH / "total_system_load.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# CBP VS HHS
# --------------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    df["Date"],
    df["Children in CBP custody"],
    label="CBP Custody"
)

plt.plot(
    df["Date"],
    df["Children in HHS Care"],
    label="HHS Care"
)

plt.title(
    "CBP Custody vs HHS Care Over Time"
)

plt.xlabel("Date")

plt.ylabel(
    "Number of Children"
)

plt.legend()

plt.xticks(rotation=45)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    FIGURES_PATH / "cbp_vs_hhs.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# TRANSFERS VS DISCHARGES
# --------------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    df["Date"],
    df["Children transferred out of CBP custody"],
    label="Transferred to HHS"
)

plt.plot(
    df["Date"],
    df["Children discharged from HHS Care"],
    label="Discharged from HHS"
)

plt.title(
    "Transfers Into HHS vs Discharges From HHS"
)

plt.xlabel("Date")

plt.ylabel(
    "Number of Children"
)

plt.legend()

plt.xticks(rotation=45)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    FIGURES_PATH / "transfers_vs_discharges.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# NET INTAKE PRESSURE
# --------------------------------------------------

plt.figure(figsize=(14, 6))

plt.axhline(
    0,
    linewidth=1
)

plt.plot(
    df["Date"],
    df["Net Intake Pressure"],
    linewidth=2
)

plt.title(
    "Net Intake Pressure Over Time"
)

plt.xlabel("Date")

plt.ylabel(
    "Transfers - Discharges"
)

plt.xticks(rotation=45)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    FIGURES_PATH / "net_intake_pressure.png",
    dpi=300
)

plt.show()


# --------------------------------------------------
# HIGH LOAD ANALYSIS
# --------------------------------------------------

flagged, threshold = identify_high_load_periods(
    df,
    percentile=90
)

high_load = flagged[
    flagged["High Load"]
].copy()

print("\n======================================")
print("HIGH-LOAD ANALYSIS")
print("======================================")

print(
    "90th percentile load threshold:",
    round(threshold, 2)
)

print(
    "Number of high-load observations:",
    len(high_load)
)

print("\nHighest-load observations:")

print(
    high_load[
        [
            "Date",
            "Total System Load",
            "Net Intake Pressure"
        ]
    ]
    .sort_values(
        "Total System Load",
        ascending=False
    )
    .head(10)
)


# --------------------------------------------------
# SAVE PROCESSED DATA
# --------------------------------------------------

processed_file = (
    OUTPUT_PATH
    / "processed_uac_data.csv"
)

df.to_csv(
    processed_file,
    index=False
)

print("\n======================================")
print("ANALYSIS COMPLETE")
print("======================================")

print(
    "Processed data saved to:"
)

print(
    processed_file
)

print(
    "\nFigures saved to:"
)

print(
    FIGURES_PATH
)