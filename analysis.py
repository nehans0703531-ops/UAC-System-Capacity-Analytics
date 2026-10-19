import pandas as pd
import numpy as np


def create_metrics(df):
    """
    Create the main UAC system capacity and care-load metrics.
    """

    df = df.copy()

    # Sort by date
    df = df.sort_values(
        "Date"
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------
    # 1. TOTAL SYSTEM LOAD
    # --------------------------------------------------

    df["Total System Load"] = (
        df["Children in CBP custody"].fillna(0)
        +
        df["Children in HHS Care"].fillna(0)
    )

    # --------------------------------------------------
    # 2. NET INTAKE PRESSURE
    # --------------------------------------------------

    df["Net Intake Pressure"] = (
        df[
            "Children transferred out of CBP custody"
        ].fillna(0)
        -
        df[
            "Children discharged from HHS Care"
        ].fillna(0)
    )

    # --------------------------------------------------
    # 3. LOAD CHANGE
    # --------------------------------------------------

    df[
        "Load Change Since Previous Report"
    ] = (
        df["Total System Load"].diff()
    )

    # --------------------------------------------------
    # 4. LOAD GROWTH RATE
    # --------------------------------------------------

    df[
        "Care Load Growth Rate (%)"
    ] = (
        df["Total System Load"]
        .pct_change()
        * 100
    )

    # --------------------------------------------------
    # 5. 7-REPORT ROLLING LOAD
    # --------------------------------------------------

    df[
        "7-Report Rolling Load"
    ] = (
        df["Total System Load"]
        .rolling(
            window=7,
            min_periods=1
        )
        .mean()
    )

    # --------------------------------------------------
    # 6. 14-REPORT ROLLING LOAD
    # --------------------------------------------------

    df[
        "14-Report Rolling Load"
    ] = (
        df["Total System Load"]
        .rolling(
            window=14,
            min_periods=1
        )
        .mean()
    )

    # --------------------------------------------------
    # 7. DISCHARGE OFFSET RATIO
    # --------------------------------------------------

    transfers = (
        df[
            "Children transferred out of CBP custody"
        ]
        .replace(
            0,
            np.nan
        )
    )

    discharges = (
        df[
            "Children discharged from HHS Care"
        ]
    )

    df[
        "Discharge Offset Ratio"
    ] = (
        discharges / transfers
    )

    # --------------------------------------------------
    # 8. CUMULATIVE NET PRESSURE
    # --------------------------------------------------

    df[
        "Cumulative Net Pressure"
    ] = (
        df[
            "Net Intake Pressure"
        ]
        .fillna(0)
        .cumsum()
    )

    return df


def summarize_kpis(df):
    """
    Generate summary KPI values.
    """

    if df.empty:
        return {}

    latest = df.iloc[-1]

    kpis = {

        "Latest Total System Load":
            latest["Total System Load"],

        "Latest CBP Custody":
            latest["Children in CBP custody"],

        "Latest HHS Care":
            latest["Children in HHS Care"],

        "Latest Net Intake Pressure":
            latest["Net Intake Pressure"],

        "Maximum Total System Load":
            df["Total System Load"].max(),

        "Average Total System Load":
            df["Total System Load"].mean(),

        "Average Net Intake Pressure":
            df["Net Intake Pressure"].mean()
    }

    return kpis


def identify_high_load_periods(
    df,
    percentile=90
):
    """
    Identify observations with relatively high
    system load.

    This uses a statistical percentile and does NOT
    represent an official capacity limit.
    """

    df = df.copy()

    # Calculate threshold
    threshold = (
        df[
            "Total System Load"
        ]
        .quantile(
            percentile / 100
        )
    )

    # Mark high-load observations
    df["High Load"] = (
        df[
            "Total System Load"
        ]
        >= threshold
    )

    return df, threshold