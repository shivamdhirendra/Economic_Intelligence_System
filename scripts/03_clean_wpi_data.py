import pandas as pd

# ============================================================
# 1. LOAD OLD WPI — BASE 2011-12
# ============================================================

old_wpi = pd.read_excel("../data/raw/monthly_index_202606.xls", header=None)

# Find the "All commodities" row
old_row = old_wpi[
    old_wpi.iloc[:, 0].astype(str).str.strip().str.lower().eq("all commodities")
].iloc[0]

# Extract monthly columns
old_data = old_row.iloc[3:].copy()

old_dates = []
old_values = []

for column, value in old_data.items():

    column_name = str(old_wpi.iloc[0, column]).strip()

    if column_name.startswith("INDX"):

        # Example: INDX042012 = April 2012
        date_string = column_name.replace("INDX", "")

        month = int(date_string[:2])
        year = int(date_string[2:])

        date = pd.Timestamp(year=year, month=month, day=1)

        old_dates.append(date)
        old_values.append(pd.to_numeric(value, errors="coerce"))

old_clean = pd.DataFrame({"Date": old_dates, "WPI_Index": old_values})

# Calculate YoY first using the full historical series
old_clean["WPI_Inflation"] = old_clean["WPI_Index"].pct_change(12) * 100

# Keep only the period required for our project
old_clean = old_clean[
    (old_clean["Date"] >= "2015-01-01") & (old_clean["Date"] <= "2026-04-01")
].copy()


# ============================================================
# 2. LOAD NEW WPI — BASE 2022-23
# ============================================================

new_wpi = pd.read_excel("../data/raw/wpi_monthly_index_202609.xlsx", header=None)

# Find the "All Commodities" row
new_row = new_wpi[
    new_wpi.iloc[:, 1].astype(str).str.strip().str.lower().eq("all commodities")
].iloc[0]

# Extract monthly columns
new_data = new_row.iloc[3:].copy()

new_dates = []
new_values = []

for column, value in new_data.items():

    column_name = str(new_wpi.iloc[0, column]).strip()

    try:
        date = pd.to_datetime(column_name, format="%b-%y")

        value = pd.to_numeric(value, errors="coerce")

        new_dates.append(date)
        new_values.append(value)

    except:
        pass

new_clean = pd.DataFrame({"Date": new_dates, "WPI_Index": new_values})

# Sort
new_clean = new_clean.sort_values("Date")

# Calculate YoY inflation
new_clean["WPI_Inflation"] = new_clean["WPI_Index"].pct_change(12) * 100

# We only need the new series from May 2026 onward
new_clean = new_clean[
    (new_clean["Date"] >= "2026-05-01") & (new_clean["Date"] <= "2026-08-01")
].copy()


# ============================================================
# 3. COMBINE OLD + NEW SERIES
# ============================================================

wpi = pd.concat(
    [old_clean[["Date", "WPI_Inflation"]], new_clean[["Date", "WPI_Inflation"]]],
    ignore_index=True,
)

wpi = wpi.sort_values("Date").reset_index(drop=True)


# ============================================================
# 4. CHECK RESULTS
# ============================================================

print("\n===== WPI DATA =====")
print(wpi.head(15))

print("\n===== LAST 15 OBSERVATIONS =====")
print(wpi.tail(15))

print("\n===== MISSING VALUES =====")
print(wpi.isna().sum())

print("\n===== SHAPE =====")
print(wpi.shape)

print("\n===== DATE RANGE =====")
print(wpi["Date"].min())
print(wpi["Date"].max())


# ============================================================
# 5. SAVE
# ============================================================

wpi.to_csv("../data/raw/wpi_inflation_monthly.csv", index=False)

print("\n===== MISSING VALUES =====")
print(wpi.isna().sum())

print("\n===== 2026 WPI =====")
print(wpi[wpi["Date"] >= "2026-01-01"].to_string(index=False))
