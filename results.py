import pandas as pd

from preprocessing import load_and_clean_data
from analysis import create_metrics


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = (
    "data/"
    "HHS_Unaccompanied_Alien_Children_Program.csv"
)

df = load_and_clean_data(DATA_PATH)

df = create_metrics(df)


# ============================================================
# BASIC STATISTICS
# ============================================================

print("\n")
print("=" * 60)
print("UAC SYSTEM CAPACITY & CARE LOAD ANALYSIS")
print("=" * 60)


print("\nDATASET INFORMATION")
print("-" * 60)

print(
    "Number of observations:",
    len(df)
)

print(
    "Start date:",
    df["Date"].min().date()
)

print(
    "End date:",
    df["Date"].max().date()
)


# ============================================================
# SYSTEM LOAD
# ============================================================

print("\nSYSTEM LOAD")
print("-" * 60)

print(
    "Average total system load:",
    round(
        df["Total System Load"].mean(),
        2
    )
)

print(
    "Maximum total system load:",
    round(
        df["Total System Load"].max(),
        2
    )
)

print(
    "Minimum total system load:",
    round(
        df["Total System Load"].min(),
        2
    )
)


# ============================================================
# MAXIMUM LOAD PERIOD
# ============================================================

max_load_row = df.loc[
    df["Total System Load"].idxmax()
]

print("\nHIGHEST SYSTEM LOAD")
print("-" * 60)

print(
    "Date:",
    max_load_row["Date"].date()
)

print(
    "Total system load:",
    round(
        max_load_row["Total System Load"],
        2
    )
)

print(
    "CBP custody:",
    round(
        max_load_row[
            "Children in CBP custody"
        ],
        2
    )
)

print(
    "HHS care:",
    round(
        max_load_row[
            "Children in HHS Care"
        ],
        2
    )
)


# ============================================================
# CBP STATISTICS
# ============================================================

print("\nCBP CUSTODY")
print("-" * 60)

print(
    "Average:",
    round(
        df[
            "Children in CBP custody"
        ].mean(),
        2
    )
)

print(
    "Maximum:",
    round(
        df[
            "Children in CBP custody"
        ].max(),
        2
    )
)


# ============================================================
# HHS STATISTICS
# ============================================================

print("\nHHS CARE")
print("-" * 60)

print(
    "Average:",
    round(
        df[
            "Children in HHS Care"
        ].mean(),
        2
    )
)

print(
    "Maximum:",
    round(
        df[
            "Children in HHS Care"
        ].max(),
        2
    )
)

print(
    "Minimum:",
    round(
        df[
            "Children in HHS Care"
        ].min(),
        2
    )
)


# ============================================================
# TRANSFERS
# ============================================================

print("\nTRANSFERS")
print("-" * 60)

print(
    "Average transfers:",
    round(
        df[
            "Children transferred out of CBP custody"
        ].mean(),
        2
    )
)

print(
    "Maximum transfers:",
    round(
        df[
            "Children transferred out of CBP custody"
        ].max(),
        2
    )
)


# ============================================================
# DISCHARGES
# ============================================================

print("\nDISCHARGES")
print("-" * 60)

print(
    "Average discharges:",
    round(
        df[
            "Children discharged from HHS Care"
        ].mean(),
        2
    )
)

print(
    "Maximum discharges:",
    round(
        df[
            "Children discharged from HHS Care"
        ].max(),
        2
    )
)


# ============================================================
# NET INTAKE PRESSURE
# ============================================================

print("\nNET INTAKE PRESSURE")
print("-" * 60)

print(
    "Average:",
    round(
        df[
            "Net Intake Pressure"
        ].mean(),
        2
    )
)

print(
    "Maximum:",
    round(
        df[
            "Net Intake Pressure"
        ].max(),
        2
    )
)

print(
    "Minimum:",
    round(
        df[
            "Net Intake Pressure"
        ].min(),
        2
    )
)


# ============================================================
# HIGH LOAD
# ============================================================

threshold = df[
    "Total System Load"
].quantile(0.90)

high_load_count = (
    df[
        "Total System Load"
    ] >= threshold
).sum()

print("\nHIGH-LOAD ANALYSIS")
print("-" * 60)

print(
    "90th percentile threshold:",
    round(threshold, 2)
)

print(
    "Number of high-load observations:",
    high_load_count
)


# ============================================================
# FINAL OBSERVATION
# ============================================================

latest = df.iloc[-1]

print("\nLATEST OBSERVATION")
print("-" * 60)

print(
    "Date:",
    latest["Date"].date()
)

print(
    "Total system load:",
    latest["Total System Load"]
)

print(
    "CBP custody:",
    latest[
        "Children in CBP custody"
    ]
)

print(
    "HHS care:",
    latest[
        "Children in HHS Care"
    ]
)

print(
    "Net intake pressure:",
    latest[
        "Net Intake Pressure"
    ]
)


print("\n")
print("=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)