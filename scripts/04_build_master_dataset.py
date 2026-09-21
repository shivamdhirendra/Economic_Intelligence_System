import pandas as pd

# ============================================================
# 1. LOAD ECONOMIC DATA
# ============================================================

economic = pd.read_csv("../data/raw/economic_data_monthly.csv")

economic["Date"] = pd.to_datetime(economic["Date"])

print("\n===== ECONOMIC DATA =====")
print(economic.head())


# ============================================================
# 2. LOAD WPI DATA
# ============================================================

wpi = pd.read_csv("../data/raw/wpi_inflation_monthly.csv")

wpi["Date"] = pd.to_datetime(wpi["Date"])

print("\n===== WPI DATA =====")
print(wpi.head())


# ============================================================
# 3. LOAD MARKET DATA
# ============================================================

market = pd.read_csv("../data/raw/market_data_monthly.csv")

# Market Date is currently YYYY-MM
market["Date"] = pd.to_datetime(market["Date"] + "-01")

print("\n===== MARKET DATA =====")
print(market.head())


# ============================================================
# 4. MERGE ECONOMIC + WPI
# ============================================================

master = economic.merge(wpi, on="Date", how="inner")


# ============================================================
# 5. MERGE MARKET DATA
# ============================================================

master = master.merge(market, on="Date", how="inner")


# ============================================================
# 6. SORT
# ============================================================

master = master.sort_values("Date").reset_index(drop=True)


# ============================================================
# 7. KEEP PROJECT PERIOD
# ============================================================

master = master[
    (master["Date"] >= "2015-01-01") & (master["Date"] <= "2026-08-01")
].copy()


# ============================================================
# 8. CHECK DATA
# ============================================================

print("\n===== MASTER DATASET =====")
print(master.head(10))

print("\n===== LAST 10 OBSERVATIONS =====")
print(master.tail(10))

print("\n===== COLUMNS =====")
print(master.columns.tolist())

print("\n===== SHAPE =====")
print(master.shape)

print("\n===== DATE RANGE =====")
print(master["Date"].min())
print(master["Date"].max())

print("\n===== MISSING VALUES =====")
print(master.isna().sum())


# ============================================================
# 9. DESCRIPTIVE STATISTICS
# ============================================================

print("\n===== DESCRIPTIVE STATISTICS =====")
print(master.describe())


# ============================================================
# 10. SAVE MASTER DATASET
# ============================================================

master.to_csv("../data/processed/master_macro_dataset.csv", index=False)
