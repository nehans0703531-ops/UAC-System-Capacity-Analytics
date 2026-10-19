import pandas as pd
import numpy as np

from statsmodels.tsa.holtwinters import ExponentialSmoothing


def prepare_forecasting_data(df):

    forecast_df = df[
        [
            "Date",
            "Total System Load"
        ]
    ].dropna().copy()

    forecast_df = forecast_df.sort_values(
        "Date"
    ).reset_index(drop=True)

    return forecast_df


# ============================================================
# MOVING AVERAGE BASELINE
# ============================================================

def moving_average_forecast(
    df,
    periods=7,
    horizon=14
):

    data = prepare_forecasting_data(df)

    if data.empty:
        raise ValueError(
            "No valid data available for forecasting."
        )

    periods = min(
        periods,
        len(data)
    )

    forecast_value = (
        data["Total System Load"]
        .tail(periods)
        .mean()
    )

    last_date = data["Date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=horizon,
        freq="D"
    )

    forecast = pd.DataFrame(
        {
            "Date": future_dates,
            "Forecast Total System Load":
                forecast_value
        }
    )

    return forecast


# ============================================================
# HOLT EXPONENTIAL SMOOTHING
# ============================================================

def exponential_smoothing_forecast(
    df,
    horizon=14
):

    data = prepare_forecasting_data(df)

    if len(data) < 5:

        raise ValueError(
            "At least 5 observations are required "
            "for exponential smoothing."
        )

    values = (
        data["Total System Load"]
        .astype(float)
        .values
    )

    model = ExponentialSmoothing(
        values,
        trend="add",
        damped_trend=True,
        initialization_method="estimated"
    )

    fitted_model = model.fit(
        optimized=True
    )

    forecast_values = fitted_model.forecast(
        horizon
    )

    forecast_values = np.maximum(
        forecast_values,
        0
    )

    last_date = data["Date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=horizon,
        freq="D"
    )

    forecast = pd.DataFrame(
        {
            "Date": future_dates,
            "Forecast Total System Load":
                forecast_values
        }
    )

    return forecast