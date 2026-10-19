import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from preprocessing import load_and_clean_data, validate_data
from analysis import (
    create_metrics,
    identify_high_load_periods,
    summarize_kpis
)
from forecasting import moving_average_forecast


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UAC System Capacity Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_PATH = Path(__file__).resolve().parent

DATA_PATH = (
    PROJECT_PATH
    / "data"
    / "HHS_Unaccompanied_Alien_Children_Program.csv"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "System Capacity & Care Load Analytics "
    "for Unaccompanied Children"
)

st.caption(
    "Data-driven monitoring of CBP custody, HHS care, "
    "transfers, discharges, system load and relative "
    "high-load periods."
)


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_and_clean_data(DATA_PATH)

except Exception as e:

    st.error(
        f"Unable to load the dataset: {e}"
    )

    st.stop()


# ============================================================
# CREATE METRICS
# ============================================================

df = create_metrics(df)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Dashboard Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# Make sure two dates are selected

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = pd.Timestamp(
        date_range[1]
    )

else:

    start_date = pd.Timestamp(
        min_date
    )

    end_date = pd.Timestamp(
        max_date
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["Date"] >= start_date)
    &
    (df["Date"] <= end_date)
].copy()


# ============================================================
# CHECK EMPTY DATA
# ============================================================

if filtered_df.empty:

    st.warning(
        "No data is available for the selected date range."
    )

    st.stop()


# ============================================================
# LATEST OBSERVATION
# ============================================================

latest = filtered_df.iloc[-1]


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Children Under Care",
        f"{latest['Total System Load']:,.0f}"
    )


with col2:

    st.metric(
        "CBP Custody",
        f"{latest['Children in CBP custody']:,.0f}"
    )


with col3:

    st.metric(
        "HHS Care",
        f"{latest['Children in HHS Care']:,.0f}"
    )


with col4:

    st.metric(
        "Net Intake Pressure",
        f"{latest['Net Intake Pressure']:,.0f}"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 System Load",
        "🏢 CBP vs HHS",
        "🔄 Intake & Discharge",
        "🚨 High-Load Analysis",
        "🔮 Forecast"
    ]
)


# ============================================================
# TAB 1 — SYSTEM LOAD
# ============================================================

with tab1:

    st.subheader(
        "Total System Care Load"
    )

    fig_load = px.line(
        filtered_df,
        x="Date",
        y=[
            "Total System Load",
            "7-Report Rolling Load",
            "14-Report Rolling Load"
        ],
        title="Total UAC System Care Load Over Time"
    )

    fig_load.update_layout(
        xaxis_title="Date",
        yaxis_title="Children Under Care",
        legend_title="Metric"
    )

    st.plotly_chart(
        fig_load,
        use_container_width=True
    )


    st.subheader(
        "Cumulative Net Intake Pressure"
    )

    fig_cumulative = px.line(
        filtered_df,
        x="Date",
        y="Cumulative Net Pressure",
        title="Cumulative Net Intake Pressure"
    )

    fig_cumulative.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Pressure"
    )

    st.plotly_chart(
        fig_cumulative,
        use_container_width=True
    )


# ============================================================
# TAB 2 — CBP VS HHS
# ============================================================

with tab2:

    st.subheader(
        "CBP Custody vs HHS Care"
    )

    fig_care = px.line(
        filtered_df,
        x="Date",
        y=[
            "Children in CBP custody",
            "Children in HHS Care"
        ],
        title="CBP Custody vs HHS Care"
    )

    fig_care.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Children"
    )

    st.plotly_chart(
        fig_care,
        use_container_width=True
    )


    st.subheader(
        "Current Care Distribution"
    )

    distribution = pd.DataFrame(
        {
            "Category": [
                "CBP Custody",
                "HHS Care"
            ],
            "Children": [
                latest[
                    "Children in CBP custody"
                ],
                latest[
                    "Children in HHS Care"
                ]
            ]
        }
    )

    fig_pie = px.pie(
        distribution,
        names="Category",
        values="Children",
        title="Latest System Care Distribution"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


# ============================================================
# TAB 3 — INTAKE & DISCHARGE
# ============================================================

with tab3:

    st.subheader(
        "Transfers vs Discharges"
    )

    fig_flow = px.line(
        filtered_df,
        x="Date",
        y=[
            "Children transferred out of CBP custody",
            "Children discharged from HHS Care"
        ],
        title="Transfers Out of CBP vs HHS Discharges"
    )

    fig_flow.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Children"
    )

    st.plotly_chart(
        fig_flow,
        use_container_width=True
    )


    st.subheader(
        "Net Intake Pressure"
    )

    fig_pressure = px.bar(
        filtered_df,
        x="Date",
        y="Net Intake Pressure",
        title="Net Intake Pressure Over Time"
    )

    fig_pressure.add_hline(
        y=0,
        line_dash="dash"
    )

    fig_pressure.update_layout(
        xaxis_title="Date",
        yaxis_title="Transfers - Discharges"
    )

    st.plotly_chart(
        fig_pressure,
        use_container_width=True
    )


# ============================================================
# TAB 4 — HIGH LOAD
# ============================================================

with tab4:

    st.subheader(
        "Relative High-Load Analysis"
    )

    high_load_df, threshold = (
        identify_high_load_periods(
            filtered_df,
            percentile=90
        )
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "90th Percentile Load Threshold",
            f"{threshold:,.0f}"
        )


    with col2:

        st.metric(
            "High-Load Observations",
            int(
                high_load_df[
                    "High Load"
                ].sum()
            )
        )


    fig_high = px.scatter(
        high_load_df,
        x="Date",
        y="Total System Load",
        color="High Load",
        title="Relative High-Load Observations"
    )

    st.plotly_chart(
        fig_high,
        use_container_width=True
    )


    st.info(
        "High-load periods are identified statistically "
        "using the 90th percentile of observed system load. "
        "This should not be interpreted as an official "
        "capacity or overcapacity threshold."
    )


# ============================================================
# TAB 5 — FORECAST
# ============================================================

with tab5:

    st.subheader(
        "14-Day Baseline Forecast"
    )

    forecast = moving_average_forecast(
        filtered_df,
        periods=7,
        horizon=14
    )


    st.dataframe(
        forecast,
        use_container_width=True
    )


    historical = filtered_df[
        [
            "Date",
            "Total System Load"
        ]
    ].copy()

    historical["Type"] = "Observed"


    future = forecast.rename(
        columns={
            "Forecast Total System Load":
            "Total System Load"
        }
    )

    future["Type"] = "Forecast"


    combined = pd.concat(
        [
            historical,
            future
        ],
        ignore_index=True
    )


    fig_forecast = px.line(
        combined,
        x="Date",
        y="Total System Load",
        color="Type",
        title="Observed vs 14-Day Forecast"
    )


    fig_forecast.update_layout(
        xaxis_title="Date",
        yaxis_title="Children Under Care"
    )


    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )


    st.info(
        "The current forecast is a simple moving-average "
        "baseline intended for exploratory planning. "
        "It is not an official prediction of future demand."
    )


# ============================================================
# DATA QUALITY
# ============================================================

st.divider()

with st.expander(
    "🔍 View Data Quality Report"
):

    quality = validate_data(df)

    quality_df = pd.DataFrame(
        list(quality.items()),
        columns=[
            "Check",
            "Result"
        ]
    )

    st.dataframe(
        quality_df,
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "System Capacity & Care Load Analytics for "
    "Unaccompanied Children | Analytical dashboard"
)