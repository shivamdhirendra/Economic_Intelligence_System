import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("../data/processed/model_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)


# ============================================================
# 2. DEFINE FEATURES AND TARGET
# ============================================================

features = [
    "Inflation_Lag1",
    "RepoRate_Lag1",
    "WPI_Inflation_Lag1",
    "NIFTY_Return_Lag1",
    "IndiaVIX_Lag1",
]

target = "Inflation"


# ============================================================
# 3. TIME-BASED SPLIT
# ============================================================

train = df[df["Date"] <= "2022-12-01"].copy()

validation = df[(df["Date"] >= "2023-01-01") & (df["Date"] <= "2024-12-01")].copy()

test = df[df["Date"] >= "2025-01-01"].copy()


print("\n===== DATA SPLIT =====")
print("Train:", train.shape)
print("Validation:", validation.shape)
print("Test:", test.shape)

print("\nTrain period:")
print(train["Date"].min(), "to", train["Date"].max())

print("\nValidation period:")
print(validation["Date"].min(), "to", validation["Date"].max())

print("\nTest period:")
print(test["Date"].min(), "to", test["Date"].max())


# ============================================================
# 4. PREPARE OLS DATA
# ============================================================

X_train = train[features]
y_train = train[target]

X_validation = validation[features]
y_validation = validation[target]

X_test = test[features]
y_test = test[target]


# Add intercept
X_train_ols = sm.add_constant(X_train)

X_validation_ols = sm.add_constant(X_validation)

X_test_ols = sm.add_constant(X_test)


# ============================================================
# 5. ESTIMATE OLS MODEL
# ============================================================

model = sm.OLS(y_train, X_train_ols).fit()


# ============================================================
# 6. MODEL SUMMARY
# ============================================================

print("\n===== OLS MODEL =====")
print(model.summary())


# ============================================================
# 7. VALIDATION PREDICTIONS
# ============================================================

validation_predictions = model.predict(X_validation_ols)

validation_mae = mean_absolute_error(y_validation, validation_predictions)

validation_rmse = np.sqrt(mean_squared_error(y_validation, validation_predictions))


# ============================================================
# 8. TEST PREDICTIONS
# ============================================================

test_predictions = model.predict(X_test_ols)

test_mae = mean_absolute_error(y_test, test_predictions)

test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))


# ============================================================
# 9. RESULTS
# ============================================================

print("\n===== OLS PERFORMANCE =====")

print("\nValidation MAE:", round(validation_mae, 4))
print("Validation RMSE:", round(validation_rmse, 4))

print("\nTest MAE:", round(test_mae, 4))
print("Test RMSE:", round(test_rmse, 4))


# ============================================================
# 10. SAVE TEST PREDICTIONS
# ============================================================

results = test[["Date", "Inflation"]].copy()

results["OLS_Predicted_Inflation"] = test_predictions

results.to_csv("../data/processed/ols_test_predictions.csv", index=False)

print("\nOLS analysis completed.")
