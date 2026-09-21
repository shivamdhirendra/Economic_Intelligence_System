import pandas as pd
import yfinance as yf

# --------------------------------------------------
# 1. Download NIFTY 50 data
# --------------------------------------------------

nifty = yf.download(
    "^NSEI", start="2015-01-01", end="2026-08-31", auto_adjust=False, progress=False
)

# Keep closing price
nifty = nifty[["Close"]].copy()
nifty.columns = ["NIFTY_Close"]

# Calculate daily return
nifty["NIFTY_Return"] = nifty["NIFTY_Close"].pct_change() * 100

# Convert daily data to monthly
nifty_monthly = nifty.resample("ME").agg(
    {"NIFTY_Close": "last", "NIFTY_Return": "mean"}
)

# --------------------------------------------------
# 2. Download India VIX
# --------------------------------------------------

vix = yf.download(
    "^INDIAVIX", start="2015-01-01", end="2026-08-31", auto_adjust=False, progress=False
)

vix = vix[["Close"]].copy()
vix.columns = ["IndiaVIX"]

# Monthly average VIX
vix_monthly = vix.resample("ME").mean()

# --------------------------------------------------
# 3. Combine NIFTY + VIX
# --------------------------------------------------

market_data = nifty_monthly.join(vix_monthly, how="inner")

# Make Date a normal column
market_data = market_data.reset_index()

# Format date
market_data["Date"] = market_data["Date"].dt.to_period("M").astype(str)

# --------------------------------------------------
# 4. Save
# --------------------------------------------------

output_path = "../data/raw/market_data_monthly.csv"

market_data.to_csv(output_path, index=False)

print("Market data downloaded successfully.")
print()
print(market_data.head())
print()
print("Shape:", market_data.shape)
print()
print("Saved to:", output_path)
