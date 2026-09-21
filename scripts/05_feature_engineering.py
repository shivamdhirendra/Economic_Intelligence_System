import pandas as pd

# ============================================================
# 1. LOAD MASTER DATASET
# ============================================================

master = pd.read_csv("../data/processed/master_macro_dataset.csv")

master["Date"] = pd.to_datetime(master["Date"])

master = master.sort_values("Date").reset_index(drop=True)


# ============================================================
# 2. CREATE LAGGED FEATURES
# ============================================================

master["Inflation_Lag1"] = master["Inflation"].shift(1)

master["RepoRate_Lag1"] = master["RepoRate"].shift(1)

master["WPI_Inflation_Lag1"] = master["WPI_Inflation"].shift(1)

master["NIFTY_Return_Lag1"] = master["NIFTY_Return"].shift(1)

master["IndiaVIX_Lag1"] = master["IndiaVIX"].shift(1)


# ============================================================
# 3. REMOVE FIRST ROW
# ============================================================

model_data = master.dropna().copy()


# ============================================================
# 4. SELECT MODEL VARIABLES
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
# 5. CHECK DATA
# ============================================================

print("\n===== MODEL DATA =====")
print(model_data.head())

print("\n===== MODEL DATA COLUMNS =====")
print(model_data.columns.tolist())

print("\n===== SHAPE =====")
print(model_data.shape)

print("\n===== MISSING VALUES =====")
print(model_data[features + [target]].isna().sum())

print("\n===== FEATURES =====")
print(features)

print("\n===== TARGET =====")
print(target)


# ============================================================
# 6. SAVE MODEL DATA
# ============================================================

model_data.to_csv("../data/processed/model_data.csv", index=False)
