import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# 1. LOAD MODEL DATA
# ============================================================

df = pd.read_csv("../data/processed/model_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)


# ============================================================
# 2. FEATURES AND TARGET
# ============================================================

features = [
    "Inflation_Lag1",
    "RepoRate_Lag1",
    "WPI_Inflation_Lag1",
    "NIFTY_Return_Lag1",
    "IndiaVIX_Lag1",
]

target = "Inflation"


X = df[features]
y = df[target]


# ============================================================
# 3. TIME-BASED SPLIT
# ============================================================

train_mask = df["Date"] <= "2022-12-01"

validation_mask = (df["Date"] >= "2023-01-01") & (df["Date"] <= "2024-12-01")

test_mask = df["Date"] >= "2025-01-01"


X_train = X[train_mask]
y_train = y[train_mask]

X_validation = X[validation_mask]
y_validation = y[validation_mask]

X_test = X[test_mask]
y_test = y[test_mask]


print("\n===== DATA SPLIT =====")
print("Train:", X_train.shape)
print("Validation:", X_validation.shape)
print("Test:", X_test.shape)


# ============================================================
# 4. RANDOM FOREST
# ============================================================

rf_model = RandomForestRegressor(
    n_estimators=300, max_depth=5, min_samples_leaf=3, random_state=42
)

rf_model.fit(X_train, y_train)

rf_validation_pred = rf_model.predict(X_validation)

rf_test_pred = rf_model.predict(X_test)


# ============================================================
# 5. GRADIENT BOOSTING
# ============================================================

gb_model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.03,
    max_depth=2,
    min_samples_leaf=3,
    random_state=42,
)

gb_model.fit(X_train, y_train)

gb_validation_pred = gb_model.predict(X_validation)

gb_test_pred = gb_model.predict(X_test)


# ============================================================
# 6. EVALUATION FUNCTION
# ============================================================


def evaluate_model(name, actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(mean_squared_error(actual, predicted))

    r2 = r2_score(actual, predicted)

    return {"Model": name, "MAE": mae, "RMSE": rmse, "R2": r2}


# ============================================================
# 7. VALIDATION RESULTS
# ============================================================

validation_results = pd.DataFrame(
    [
        evaluate_model("Random Forest", y_validation, rf_validation_pred),
        evaluate_model("Gradient Boosting", y_validation, gb_validation_pred),
    ]
)


print("\n===== VALIDATION RESULTS =====")
print(validation_results.round(4))


# ============================================================
# 8. TEST RESULTS
# ============================================================

test_results = pd.DataFrame(
    [
        evaluate_model("Random Forest", y_test, rf_test_pred),
        evaluate_model("Gradient Boosting", y_test, gb_test_pred),
    ]
)


print("\n===== TEST RESULTS =====")
print(test_results.round(4))

# ============================================================
# 9. NAIVE PERSISTENCE BASELINE
# ============================================================

naive_test_pred = X_test["Inflation_Lag1"].values

naive_mae = mean_absolute_error(y_test, naive_test_pred)

naive_rmse = np.sqrt(mean_squared_error(y_test, naive_test_pred))

naive_r2 = r2_score(y_test, naive_test_pred)

print("\n===== NAIVE BASELINE =====")

print("Naive MAE:", round(naive_mae, 4))
print("Naive RMSE:", round(naive_rmse, 4))
print("Naive R2:", round(naive_r2, 4))


# ============================================================
# 10. FINAL MODEL COMPARISON
# ============================================================

ols_mae = 0.5352
ols_rmse = 0.7220

ols_result = pd.DataFrame(
    [{"Model": "OLS", "MAE": ols_mae, "RMSE": ols_rmse, "R2": np.nan}]
)

naive_result = pd.DataFrame(
    [
        {
            "Model": "Naive Persistence",
            "MAE": naive_mae,
            "RMSE": naive_rmse,
            "R2": naive_r2,
        }
    ]
)

comparison = pd.concat([naive_result, ols_result, test_results], ignore_index=True)

print("\n===== FINAL MODEL COMPARISON =====")
print(comparison.round(4))


# ============================================================
# 10. SAVE COMPARISON
# ============================================================

comparison.to_csv("../data/processed/model_comparison.csv", index=False)


# ============================================================
# 11. SAVE TEST PREDICTIONS
# ============================================================

predictions = df.loc[test_mask, ["Date", "Inflation"]].copy()

predictions["RandomForest_Prediction"] = rf_test_pred

predictions["GradientBoosting_Prediction"] = gb_test_pred

predictions.to_csv("../data/processed/ml_test_predictions.csv", index=False)


# ============================================================
# 12. FEATURE IMPORTANCE
# ============================================================

feature_importance = pd.DataFrame(
    {
        "Feature": features,
        "RandomForest_Importance": rf_model.feature_importances_,
        "GradientBoosting_Importance": gb_model.feature_importances_,
    }
)

feature_importance = feature_importance.sort_values(
    "RandomForest_Importance", ascending=False
)

print("\n===== FEATURE IMPORTANCE =====")
print(feature_importance.round(4))

feature_importance.to_csv("../data/processed/feature_importance.csv", index=False)


print("\nML forecasting completed successfully.")
