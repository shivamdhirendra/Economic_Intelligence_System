import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. LOAD MODEL DATA
# ============================================================

df = pd.read_csv("../data/processed/model_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")


# ============================================================
# 2. BASIC SUMMARY
# ============================================================

print("\n===== CORRELATION MATRIX =====")

variables = ["Inflation", "RepoRate", "WPI_Inflation", "NIFTY_Return", "IndiaVIX"]

print(df[variables].corr().round(3))


# ============================================================
# 3. INFLATION TREND
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(df["Date"], df["Inflation"])

plt.axhline(y=4, linestyle="--")

plt.title("India CPI Inflation")
plt.xlabel("Date")
plt.ylabel("Inflation (%)")

plt.tight_layout()
plt.savefig("../reports/CPI_trend.png", dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# 4. CPI VS WPI
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(df["Date"], df["Inflation"], label="CPI Inflation")

plt.plot(df["Date"], df["WPI_Inflation"], label="WPI Inflation")

plt.title("CPI vs WPI Inflation")
plt.xlabel("Date")
plt.ylabel("Inflation (%)")
plt.legend()

plt.tight_layout()
plt.savefig("../reports/CPI_vs_WPI.png", dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# 5. CPI VS REPO RATE
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(df["Date"], df["Inflation"], label="CPI Inflation")

plt.plot(df["Date"], df["RepoRate"], label="Repo Rate")

plt.title("CPI Inflation vs RBI Repo Rate")
plt.xlabel("Date")
plt.ylabel("Rate (%)")
plt.legend()

plt.tight_layout()
plt.savefig("../reports/CPI_vs_RepoRate.png", dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# 6. CPI VS INDIA VIX
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(df["Date"], df["Inflation"], label="CPI Inflation")

plt.plot(df["Date"], df["IndiaVIX"], label="India VIX")

plt.title("CPI Inflation vs India VIX")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()

plt.tight_layout()
plt.savefig("../reports/CPI_vs_IndiaVIX.png", dpi=300, bbox_inches="tight")
plt.show()


# ============================================================
# 7. NIFTY RETURNS VS INFLATION
# ============================================================

plt.figure(figsize=(12, 5))

plt.scatter(df["NIFTY_Return"], df["Inflation"], alpha=0.7)

plt.title("NIFTY Returns vs CPI Inflation")
plt.xlabel("NIFTY Monthly Return (%)")
plt.ylabel("CPI Inflation (%)")

plt.tight_layout()
plt.savefig("../reports/NiftyReturns_vs_CPI.png", dpi=300, bbox_inches="tight")
plt.show()
