from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "train.csv"


@st.cache_data
def load_training_data():
    return pd.read_csv(DATA_PATH, parse_dates=["Date"])


def build_forecast(store_data, horizon):
    latest_date = store_data["Date"].max()
    recent_data = store_data[store_data["Date"] >= latest_date - pd.Timedelta(days=84)]
    future_dates = pd.date_range(latest_date + pd.Timedelta(days=1), periods=horizon)
    weekday_averages = recent_data.groupby("DayOfWeek")[["Sales", "Customers"]].median()
    overall_averages = recent_data[["Sales", "Customers"]].median()

    predictions = []
    for date in future_dates:
        weekday = date.dayofweek + 1
        baseline = weekday_averages.loc[weekday] if weekday in weekday_averages.index else overall_averages
        predictions.append(
            {
                "Date": date,
                "Predicted Sales": max(0, round(float(baseline["Sales"]))),
                "Predicted Customers": max(0, round(float(baseline["Customers"]))),
            }
        )
    return pd.DataFrame(predictions)


st.set_page_config(page_title="Rossmann Forecast", page_icon="📈", layout="wide")
st.title("Rossmann Sales Forecasting")
st.caption("A weekday-aware baseline forecast for sales and customer traffic")

try:
    training_data = load_training_data()
except FileNotFoundError:
    st.error("The training data file could not be found in the data folder.")
    st.stop()

available_stores = sorted(training_data["Store"].unique())
store_id = st.sidebar.selectbox("Store", available_stores)
horizon = st.sidebar.slider("Forecast horizon (days)", 7, 42, 14)

store_data = training_data[training_data["Store"] == store_id]
forecast = build_forecast(store_data, horizon)

total_sales = forecast["Predicted Sales"].sum()
total_customers = forecast["Predicted Customers"].sum()
metric_one, metric_two, metric_three = st.columns(3)
metric_one.metric("Forecast sales", f"${total_sales:,.0f}")
metric_two.metric("Forecast customers", f"{total_customers:,.0f}")
metric_three.metric("Daily average sales", f"${forecast['Predicted Sales'].mean():,.0f}")

st.subheader(f"Store {store_id}: predicted sales and customers")
chart_data = forecast.set_index("Date")[["Predicted Sales", "Predicted Customers"]]
st.line_chart(chart_data, height=420)

st.subheader("Prediction table")
display_forecast = forecast.copy()
display_forecast["Date"] = display_forecast["Date"].dt.strftime("%Y-%m-%d")
st.dataframe(display_forecast, use_container_width=True, hide_index=True)
st.download_button(
    "Download predictions as CSV",
    data=display_forecast.to_csv(index=False).encode("utf-8"),
    file_name=f"rossmann_store_{store_id}_forecast.csv",
    mime="text/csv",
    type="primary",
)

st.caption("Forecast method: median of the selected store's most recent 12 weeks for each weekday.")



