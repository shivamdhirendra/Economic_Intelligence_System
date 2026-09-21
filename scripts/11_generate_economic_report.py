import pandas as pd

# ============================================================
# 1. LOAD DATA
# ============================================================

master = pd.read_csv("../data/processed/master_macro_dataset.csv")

master["Date"] = pd.to_datetime(master["Date"])

master = master.sort_values("Date")


comparison = pd.read_csv("../data/processed/model_comparison.csv")

forecast = pd.read_csv("../data/processed/final_forecast_results.csv")

forecast["Date"] = pd.to_datetime(forecast["Date"])


# ============================================================
# 2. LATEST ECONOMIC DATA
# ============================================================

latest = master.iloc[-1]

latest_date = latest["Date"].strftime("%B %Y")

inflation = latest["Inflation"]

repo_rate = latest["RepoRate"]

wpi = latest["WPI_Inflation"]

nifty_return = latest["NIFTY_Return"]

vix = latest["IndiaVIX"]


# ============================================================
# 3. MODEL RESULTS
# ============================================================

best_mae_model = comparison.loc[comparison["MAE"].idxmin()]

best_rmse_model = comparison.loc[comparison["RMSE"].idxmin()]


# ============================================================
# 4. LATEST FORECASTS
# ============================================================

latest_forecast = forecast.iloc[-1]

actual = latest_forecast["Inflation"]

naive_prediction = latest_forecast["Naive_Prediction"]

ols_prediction = latest_forecast["OLS_Predicted_Inflation"]

rf_prediction = latest_forecast["RandomForest_Prediction"]

gb_prediction = latest_forecast["GradientBoosting_Prediction"]


# ============================================================
# 5. BUILD REPORT
# ============================================================

report = f"""
# India Economic Intelligence Report

**Data through:** {latest_date}

---

## 1. Economic Snapshot

| Indicator | Latest Value |
|---|---:|
| CPI Inflation | {inflation:.2f}% |
| WPI Inflation | {wpi:.2f}% |
| RBI Repo Rate | {repo_rate:.2f}% |
| NIFTY Monthly Return | {nifty_return:.2f}% |
| India VIX | {vix:.2f} |

---

## 2. Inflation Forecasting

The forecasting experiment compares a persistence benchmark,
OLS regression, Random Forest, and Gradient Boosting.

### Out-of-Sample Model Performance

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
"""

for _, row in comparison.iterrows():

    r2_value = f"{row['R2']:.4f}" if pd.notna(row["R2"]) else "N/A"

    report += (
        f"| {row['Model']} | "
        f"{row['MAE']:.4f} | "
        f"{row['RMSE']:.4f} | "
        f"{r2_value} |\n"
    )


report += f"""

### Benchmark Summary

Lowest MAE: **{best_mae_model['Model']}**
({best_mae_model['MAE']:.4f})

Lowest RMSE: **{best_rmse_model['Model']}**
({best_rmse_model['RMSE']:.4f})

---

## 3. Latest Forecast Comparison

| Model | Forecast |
|---|---:|
| Actual CPI Inflation | {actual:.2f}% |
| Naive Persistence | {naive_prediction:.2f}% |
| OLS | {ols_prediction:.2f}% |
| Random Forest | {rf_prediction:.2f}% |
| Gradient Boosting | {gb_prediction:.2f}% |

---

## 4. Interpretation

The forecasting results indicate that inflation persistence is an
important component of short-term CPI inflation forecasting.

The tested nonlinear machine-learning models did not outperform
the conventional benchmarks on the final out-of-sample period.
This provides a useful comparison between traditional econometric
forecasting and machine-learning approaches.

The results should be interpreted as forecasting associations
rather than causal estimates.

---

## 5. Data Coverage

The system uses monthly Indian economic and financial data covering:

**January 2015 – August 2026**

The dataset combines:

- CPI inflation
- RBI repo rate
- WPI inflation
- NIFTY returns
- India VIX

---

*This report was generated automatically using Python.*
"""


# ============================================================
# 6. SAVE REPORT
# ============================================================

output_path = "../reports/economic_intelligence_report.md"

with open(output_path, "w", encoding="utf-8") as file:

    file.write(report)


print("\n===== REPORT GENERATED =====")
print(output_path)
