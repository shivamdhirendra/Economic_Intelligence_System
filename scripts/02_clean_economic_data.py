import pandas as pd

# ============================================================
# 1. LOAD CPI DATA
# ============================================================

cpi_back = pd.read_excel("../data/raw/cpi1.xlsx")
cpi_current = pd.read_excel("../data/raw/cpi2.xlsx")

# ------------------------------------------------------------
# CPI BACK SERIES: 2015-2024
# ------------------------------------------------------------

cpi_back = cpi_back[(cpi_back["year"] >= 2015) & (cpi_back["year"] <= 2024)].copy()

cpi_back = cpi_back[["year", "month", "index", "inflation"]].copy()

cpi_back.rename(columns={"inflation": "Inflation"}, inplace=True)

# ------------------------------------------------------------
# CPI 2025
# Official current series has index values but blank
# inflation values, so calculate YoY inflation ourselves.
# ------------------------------------------------------------

cpi_2024_index = cpi_back[cpi_back["year"] == 2024][["month", "index"]].copy()

cpi_2024_index.rename(columns={"index": "CPI_2024"}, inplace=True)

cpi_2025 = cpi_current[cpi_current["year"] == 2025][["year", "month", "index"]].copy()

cpi_2025.rename(columns={"index": "CPI_2025"}, inplace=True)

cpi_2025 = cpi_2025.merge(cpi_2024_index, on="month", how="left")

cpi_2025["Inflation"] = ((cpi_2025["CPI_2025"] / cpi_2025["CPI_2024"]) - 1) * 100

cpi_2025 = cpi_2025[["year", "month", "Inflation"]]

# ------------------------------------------------------------
# CPI 2026
# January-August 2026
# These already have inflation values.
# ------------------------------------------------------------

cpi_2026 = cpi_current[
    (cpi_current["year"] == 2026)
    & (
        cpi_current["month"].isin(
            ["January", "February", "March", "April", "May", "June", "July", "August"]
        )
    )
][["year", "month", "inflation"]].copy()

cpi_2026.rename(columns={"inflation": "Inflation"}, inplace=True)

# ------------------------------------------------------------
# COMBINE CPI
# ------------------------------------------------------------

cpi = pd.concat(
    [cpi_back[["year", "month", "Inflation"]], cpi_2025, cpi_2026], ignore_index=True
)

# Convert month names to actual dates
cpi["Date"] = pd.to_datetime(cpi["year"].astype(str) + "-" + cpi["month"] + "-01")

cpi = cpi[["Date", "Inflation"]].sort_values("Date")

# ============================================================
# 2. LOAD RBI POLICY RATES
# ============================================================

rbi = pd.read_excel("../data/raw/rbi_policy_rates_raw.xlsx", header=None)

##print("\nRBI FILE PREVIEW:")
##print(rbi.iloc[:20, :10].to_string())

# Row 5 contains the main headers.
# Column 1 = Effective Date
# Column 3 = Repo Rate

repo = rbi.iloc[8:, [1, 3]].copy()

repo.columns = ["Date", "RepoRate"]

repo["Date"] = pd.to_datetime(repo["Date"], errors="coerce")

# Remove invalid rows
repo = repo.dropna(subset=["Date"])

# Convert "-" to missing
repo["RepoRate"] = pd.to_numeric(repo["RepoRate"], errors="coerce")

# Sort chronologically
repo = repo.sort_values("Date")

# Keep 2015 onward
repo = repo[repo["Date"] >= "2015-01-01"].copy()

# Carry the latest announced repo rate forward.
# RBI only records a value when the rate changes.
repo["RepoRate"] = repo["RepoRate"].ffill()

# ============================================================
# 3. CREATE MONTHLY REPO RATE
# ============================================================

repo_monthly = (
    repo.set_index("Date").resample("ME")["RepoRate"].last().ffill().reset_index()
)

# Convert month-end date to month-start date
# so it matches the CPI dataset.
repo_monthly["Date"] = repo_monthly["Date"].dt.to_period("M").dt.to_timestamp()

# ============================================================
# 4. ADD 2026 REPO RATE
# ============================================================

dates_2026 = pd.date_range(start="2026-01-01", end="2026-08-01", freq="MS")

repo_2026 = pd.DataFrame({"Date": dates_2026, "RepoRate": 5.25})

repo_monthly = pd.concat([repo_monthly, repo_2026], ignore_index=True)

# ============================================================
# 5. MERGE CPI + REPO RATE
# ============================================================

economic_data = cpi.merge(repo_monthly, on="Date", how="left")

# ============================================================
# 6. KEEP OUR PROJECT PERIOD
# ============================================================

economic_data = economic_data[
    (economic_data["Date"] >= "2015-01-01") & (economic_data["Date"] <= "2026-08-31")
].copy()

# ============================================================
# 7. CHECK DATA
# ============================================================

print("\nEconomic data:")
print(economic_data.head())

print("\nLast observations:")
print(economic_data.tail())

print("\nShape:")
print(economic_data.shape)

print("\nMissing values:")
print(economic_data.isna().sum())

# ============================================================
# 8. SAVE
# ============================================================

economic_data.to_csv("../data/raw/economic_data_monthly.csv", index=False)
