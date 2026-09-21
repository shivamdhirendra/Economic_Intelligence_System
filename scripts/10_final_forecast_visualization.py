import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. LOAD TEST DATA
# ============================================================

model_data = pd.read_csv("../data/processed/model_data.csv")

model_data["Date"] = pd.to_datetime(model_data["Date"])

model_data = model_data.sort_values("Date")


# Test period
test = model_data[model_data["Date"] >= "2025-01-01"].copy()


# ============================================================
# 2. LOAD OLS PREDICTIONS
# ============================================================

ols = pd.read_csv("../data/processed/ols_test_predictions.csv")

ols["Date"] = pd.to_datetime(ols["Date"])


# ============================================================
# 3. LOAD ML PREDICTIONS
# ============================================================

ml = pd.read_csv("../data/processed/ml_test_predictions.csv")

ml["Date"] = pd.to_datetime(ml["Date"])


# ============================================================
# 4. COMBINE PREDICTIONS
# ============================================================

results = test[["Date", "Inflation", "Inflation_Lag1"]].copy()

results = results.merge(ols[["Date", "OLS_Predicted_Inflation"]], on="Date", how="left")

results = results.merge(
    ml[["Date", "RandomForest_Prediction", "GradientBoosting_Prediction"]],
    on="Date",
    how="left",
)


# Rename naive prediction
results["Naive_Prediction"] = results["Inflation_Lag1"]


# ============================================================
# 5. PLOT ACTUAL VS ALL MODELS
# ============================================================

plt.figure(figsize=(13, 6))

plt.plot(
    results["Date"], results["Inflation"], label="Actual CPI Inflation", linewidth=2
)

plt.plot(
    results["Date"],
    results["Naive_Prediction"],
    label="Naive Persistence",
    linestyle="--",
)

plt.plot(
    results["Date"], results["OLS_Predicted_Inflation"], label="OLS", linestyle="--"
)

plt.plot(
    results["Date"],
    results["RandomForest_Prediction"],
    label="Random Forest",
    linestyle="--",
)

plt.plot(
    results["Date"],
    results["GradientBoosting_Prediction"],
    label="Gradient Boosting",
    linestyle="--",
)

plt.title("CPI Inflation: Actual vs Model Predictions")

plt.xlabel("Date")
plt.ylabel("Inflation (%)")

plt.legend()

plt.tight_layout()

plt.savefig("../reports/final_forecast_comparison.png", dpi=300, bbox_inches="tight")

plt.show()


# ============================================================
# 6. SAVE COMBINED FORECAST DATA
# ============================================================

results.to_csv("../data/processed/final_forecast_results.csv", index=False)

print(results)
