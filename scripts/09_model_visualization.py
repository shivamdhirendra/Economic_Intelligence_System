import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. LOAD RESULTS
# ============================================================

predictions = pd.read_csv("../data/processed/ml_test_predictions.csv")

predictions["Date"] = pd.to_datetime(predictions["Date"])

comparison = pd.read_csv("../data/processed/model_comparison.csv")


# ============================================================
# 2. ACTUAL VS ML PREDICTIONS
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(predictions["Date"], predictions["Inflation"], label="Actual CPI Inflation")

plt.plot(
    predictions["Date"], predictions["RandomForest_Prediction"], label="Random Forest"
)

plt.plot(
    predictions["Date"],
    predictions["GradientBoosting_Prediction"],
    label="Gradient Boosting",
)

plt.title("Actual vs Predicted CPI Inflation")

plt.xlabel("Date")
plt.ylabel("Inflation (%)")

plt.legend()

plt.tight_layout()

plt.savefig("../reports/actual_vs_ml_predictions.png", dpi=300, bbox_inches="tight")

plt.show()


# ============================================================
# 3. MODEL PERFORMANCE — MAE
# ============================================================

plt.figure(figsize=(9, 5))

plt.bar(comparison["Model"], comparison["MAE"])

plt.title("Model Comparison — Test MAE")

plt.ylabel("Mean Absolute Error")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig("../reports/model_comparison_mae.png", dpi=300, bbox_inches="tight")

plt.show()


# ============================================================
# 4. MODEL PERFORMANCE — RMSE
# ============================================================

plt.figure(figsize=(9, 5))

plt.bar(comparison["Model"], comparison["RMSE"])

plt.title("Model Comparison — Test RMSE")

plt.ylabel("Root Mean Squared Error")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig("../reports/model_comparison_rmse.png", dpi=300, bbox_inches="tight")

plt.show()
