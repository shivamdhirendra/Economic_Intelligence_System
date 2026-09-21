
# India Economic Intelligence Report

**Data through:** August 2026

---

## 1. Economic Snapshot

| Indicator | Latest Value |
|---|---:|
| CPI Inflation | 4.82% |
| WPI Inflation | 9.92% |
| RBI Repo Rate | 5.25% |
| NIFTY Monthly Return | -0.04% |
| India VIX | 11.50 |

---

## 2. Inflation Forecasting

The forecasting experiment compares a persistence benchmark,
OLS regression, Random Forest, and Gradient Boosting.

### Out-of-Sample Model Performance

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Naive Persistence | 0.5436 | 0.6758 | 0.7341 |
| OLS | 0.5352 | 0.7220 | N/A |
| Random Forest | 0.6564 | 0.8753 | 0.5539 |
| Gradient Boosting | 1.0228 | 1.4093 | -0.1564 |


### Benchmark Summary

Lowest MAE: **OLS**
(0.5352)

Lowest RMSE: **Naive Persistence**
(0.6758)

---

## 3. Latest Forecast Comparison

| Model | Forecast |
|---|---:|
| Actual CPI Inflation | 4.82% |
| Naive Persistence | 4.45% |
| OLS | 4.45% |
| Random Forest | 4.62% |
| Gradient Boosting | 4.94% |

---

## 4. Interpretation

The forecasting results indicate that inflation persistence is an
important component of short-term CPI inflation forecasting.

The tested nonlinear machine-learning models did not outperform
the conventional benchmarks on the final out-of-sample period.
This provides a useful comparison between traditional econometric
forecasting and machine-learning approaches.

The results should be interpreted as forecasting associations
rather than causal estimates.

---

## 5. Data Coverage

The system uses monthly Indian economic and financial data covering:

**January 2015 – August 2026**

The dataset combines:

- CPI inflation
- RBI repo rate
- WPI inflation
- NIFTY returns
- India VIX

---

*This report was generated automatically using Python.*
