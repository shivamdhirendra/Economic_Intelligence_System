import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"
# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="India Economic Intelligence System", page_icon="📊", layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

master = pd.read_csv(DATA_DIR / "master_macro_dataset.csv")

master["Date"] = pd.to_datetime(master["Date"])

master = master.sort_values("Date")

comparison = pd.read_csv(DATA_DIR / "model_comparison.csv")

forecast = pd.read_csv(DATA_DIR / "final_forecast_results.csv")

forecast["Date"] = pd.to_datetime(forecast["Date"])


# ============================================================
# TITLE
# ============================================================

st.title("🇮🇳 India Economic Intelligence System")

st.markdown("""
    **Monthly macroeconomic monitoring and CPI inflation forecasting**

    Data coverage: **January 2015 – August 2026**
    """)


# ============================================================
# LATEST DATA
# ============================================================

latest = master.iloc[-1]

st.subheader(f"Economic Snapshot — {latest['Date'].strftime('%B %Y')}")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("CPI Inflation", f"{latest['Inflation']:.2f}%")

col2.metric("WPI Inflation", f"{latest['WPI_Inflation']:.2f}%")

col3.metric("Repo Rate", f"{latest['RepoRate']:.2f}%")

col4.metric("NIFTY Return", f"{latest['NIFTY_Return']:.2f}%")

col5.metric("India VIX", f"{latest['IndiaVIX']:.2f}")


# ============================================================
# CPI + WPI
# ============================================================

st.subheader("Inflation Trends")

fig = go.Figure()

fig.add_trace(go.Scatter(x=master["Date"], y=master["Inflation"], name="CPI Inflation"))

fig.add_trace(
    go.Scatter(x=master["Date"], y=master["WPI_Inflation"], name="WPI Inflation")
)

fig.update_layout(
    xaxis_title="Date", yaxis_title="Inflation (%)", hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)


# ============================================================
# REPO RATE
# ============================================================

st.subheader("RBI Repo Rate")

fig_repo = go.Figure()

fig_repo.add_trace(go.Scatter(x=master["Date"], y=master["RepoRate"], name="Repo Rate"))

fig_repo.update_layout(
    xaxis_title="Date", yaxis_title="Repo Rate (%)", hovermode="x unified"
)

st.plotly_chart(fig_repo, use_container_width=True)


# ============================================================
# MARKET INDICATORS
# ============================================================

st.subheader("Market Indicators")

col1, col2 = st.columns(2)

with col1:

    fig_nifty = go.Figure()

    fig_nifty.add_trace(
        go.Scatter(x=master["Date"], y=master["NIFTY_Return"], name="NIFTY Return")
    )

    fig_nifty.update_layout(
        title="NIFTY Monthly Return", xaxis_title="Date", yaxis_title="Return (%)"
    )

    st.plotly_chart(fig_nifty, use_container_width=True)


with col2:

    fig_vix = go.Figure()

    fig_vix.add_trace(
        go.Scatter(x=master["Date"], y=master["IndiaVIX"], name="India VIX")
    )

    fig_vix.update_layout(title="India VIX", xaxis_title="Date", yaxis_title="VIX")

    st.plotly_chart(fig_vix, use_container_width=True)


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.subheader("Forecasting Model Performance")

st.dataframe(comparison.round(4), use_container_width=True, hide_index=True)


# ============================================================
# FORECAST CHART
# ============================================================

st.subheader("CPI Inflation: Actual vs Forecasts")

fig_forecast = go.Figure()

fig_forecast.add_trace(
    go.Scatter(x=forecast["Date"], y=forecast["Inflation"], name="Actual")
)

fig_forecast.add_trace(
    go.Scatter(
        x=forecast["Date"], y=forecast["Naive_Prediction"], name="Naive Persistence"
    )
)

fig_forecast.add_trace(
    go.Scatter(x=forecast["Date"], y=forecast["OLS_Predicted_Inflation"], name="OLS")
)

fig_forecast.add_trace(
    go.Scatter(
        x=forecast["Date"], y=forecast["RandomForest_Prediction"], name="Random Forest"
    )
)

fig_forecast.add_trace(
    go.Scatter(
        x=forecast["Date"],
        y=forecast["GradientBoosting_Prediction"],
        name="Gradient Boosting",
    )
)

fig_forecast.update_layout(
    xaxis_title="Date", yaxis_title="CPI Inflation (%)", hovermode="x unified"
)

st.plotly_chart(fig_forecast, use_container_width=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Economic Intelligence System | "
    "Monthly Indian macroeconomic and financial data | "
    "2015–August 2026"
)
