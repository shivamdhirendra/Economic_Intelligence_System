# Economic Intelligence System — India Macro Forecasting
I built this project to understand whether Indian macroeconomic and financial indicators can be used to forecast monthly CPI inflation.

Instead of using a standard machine-learning dataset, I collected and combined Indian economic and market data and built the project as a small end-to-end system. It covers data collection, cleaning, exploratory analysis, econometric modelling, machine learning, automated reporting, and an interactive dashboard.

The data used in the current version covers **January 2015 to August 2026**.

## What I wanted to study
Inflation is affected by several parts of the economy, so I wanted to see how much information from previous months could help forecast current CPI inflation.

The variables I worked with were:
* CPI inflation
* WPI inflation
* RBI repo rate
* NIFTY returns
* India VIX

The main forecasting question was -> **Can lagged macroeconomic and financial variables improve short-term CPI inflation forecasts?**

## How the project works
The project follows this workflow:

Indian Economic & Financial Data
            ↓
       Data Cleaning
            ↓
      Master Dataset
            ↓
    Feature Engineering
            ↓
   Exploratory Analysis
            ↓
   Econometric Benchmark
            ↓
     ML Forecasting
            ↓
   Out-of-Sample Testing
            ↓
   Automated Economic Report
            ↓
     Streamlit Dashboard

## Data
The project uses monthly observations covering January 2015 to August 2026.

The main variables are:
| Variable      | Description                 |
| ------------- | --------------------------- |
| CPI Inflation | Consumer price inflation    |
| WPI Inflation | Wholesale price inflation   |
| Repo Rate     | RBI policy repo rate        |
| NIFTY Return  | Monthly NIFTY return        |
| India VIX     | Market volatility indicator |

The WPI data required a series transition during 2026 because the official WPI base changed from 2011–12 to 2022–23. I used the YoY inflation rates within the respective series rather than directly combining the two index levels.

## Feature Engineering
For forecasting, I used one-month lagged variables:
* Previous-month CPI inflation
* Previous-month repo rate
* Previous-month WPI inflation
* Previous-month NIFTY return
* Previous-month India VIX

The idea was to make the forecasting setup use information from the previous month rather than information from the month being predicted.
The resulting modelling dataset contains **139 usable monthly observations** after creating the one-month lags.

## Modelling Approach
I compared four approaches:
1. Naive Persistence
2. Ordinary Least Squares (OLS)
3. Random Forest
4. Gradient Boosting

The data was divided chronologically:
| Period           | Use        |
| ---------------- | ---------- |
| 2015–2022        | Training   |
| 2023–2024        | Validation |
| 2025–August 2026 | Final test |

I used a chronological split instead of randomly shuffling the observations because this is a forecasting problem.

## Results
The final test-period results were:
| Model             |    MAE |   RMSE |      R² |
| ----------------- | -----: | -----: | ------: |
| Naive Persistence | 0.5436 | 0.6758 |  0.7341 |
| OLS               | 0.5352 | 0.7220 |       — |
| Random Forest     | 0.6564 | 0.8753 |  0.5539 |
| Gradient Boosting | 1.0228 | 1.4093 | -0.1564 |

The result was not what I initially expected: the more complicated machine-learning models did **not** outperform the simpler benchmarks on the final test period.

OLS produced the lowest MAE, while the persistence benchmark produced the lowest RMSE.

The Random Forest model also relied heavily on previous-month inflation, which suggests that inflation persistence is an important part of the forecasting problem.

I kept this result rather than tuning the models until one of them produced a better number. The comparison itself is one of the useful findings of the project.

## Exploratory Analysis
The exploratory analysis looked at:
* CPI inflation over time
* CPI versus WPI inflation
* CPI versus the repo rate
* CPI versus India VIX
* NIFTY returns versus CPI inflation
* Correlations between the main variables

Some of the relationships were useful for feature selection, but they are treated as associations rather than causal relationships.

For example, CPI inflation and the repo rate had a negative correlation in the sample. This does not by itself mean that changes in the repo rate caused inflation to move in the opposite direction.

## Automated Report
The project generates an economic report automatically from the processed data and model results.

The report includes:
* Latest economic indicators
* Model performance
* Forecast comparison
* Data coverage
* A short interpretation of the results

The generated report is stored in -> reports/economic_intelligence_report.md

## Dashboard
I also built a Streamlit dashboard to make the results easier to explore.

The dashboard shows:
* Latest CPI inflation
* WPI inflation
* RBI repo rate
* NIFTY returns
* India VIX
* Historical inflation trends
* Model performance
* Actual versus predicted CPI inflation

Run it from the project root with:
```bash
streamlit run dashboard/app.py
```

## Running the Project
Clone the repository.
Install the required packages:
```bash
pip install -r requirements.txt
```
The dashboard can then be started with:
```bash
streamlit run dashboard/app.py
```
The individual scripts in the `scripts/` directory contain the different stages of the data and modelling pipeline.

## Limitations
There are a few limitations in the current version.

First, the target variable is monthly CPI inflation, so the total number of observations is relatively small for machine-learning models.

Second, the current version uses a relatively simple set of lagged financial features. The NIFTY and India VIX data could be made more informative by deriving additional monthly features from their underlying daily observations.

Third, the WPI series changes its official base during 2026, which requires care when combining the historical series.

Finally, the relationships in this project should be interpreted as forecasting relationships rather than causal estimates.

## Possible Extensions
If I continue developing the project, I would focus on:
* Creating richer monthly features from daily NIFTY and India VIX data
* Adding additional Indian macroeconomic indicators
* Testing regularized regression models
* Using rolling or walk-forward validation
* Testing additional forecasting models
* Improving the automated report
* Deploying the Streamlit dashboard

## Technologies
**Python · Pandas · NumPy · Statsmodels · Scikit-learn · Matplotlib · Plotly · Streamlit · Git · GitHub**
