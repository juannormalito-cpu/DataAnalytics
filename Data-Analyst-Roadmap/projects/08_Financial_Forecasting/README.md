# Project 08 · Financial Forecasting

**Difficulty:** Advanced · **Stack:** Python, Time Series · **Dataset:** [Rossmann Store Sales](../../datasets/CATALOG.md#chapter-07--professional-projects)

## Business Problem
CFO: *"I need a reliable revenue forecast for the next quarter across all stores, including how promotions and holidays affect it, for our budget planning."*

## Objectives
- Build a time-series forecasting model for daily/weekly sales.
- Quantify the effect of promotions and holidays.
- Provide a forecast with a confidence interval, not just a point estimate.

## Database Diagram
`fact_daily_sales` (store_id, date_id, sales, customers, promo_flag, holiday_flag) with `dim_store`, `dim_date` — per [Chapter 03](../../handbook/03_Databases.md).

## Questions to Answer
1. What's the underlying trend and seasonality in sales?
2. How much do promotions lift sales, holding other factors constant?
3. Which forecasting approach (classical time series vs. gradient boosting with time features) performs best out-of-sample?
4. How wide is the uncertainty band on the forecast, and does it widen appropriately further out?

## Workflow
- **Python** ([`python/`](python/)): decomposition (trend/seasonality), feature engineering for time series, model comparison (e.g., Prophet/SARIMA vs. XGBoost with lag features), backtesting per [Chapter 08](../../handbook/08_Machine_Learning.md).
- **Power BI** ([`powerbi/`](powerbi/)): forecast-vs-actual visualization with confidence bands.

## Expected Dashboard
A forecast dashboard: actuals vs. forecast, confidence interval band, promo-lift breakout.

## Expected Conclusions
Next-quarter revenue forecast with confidence interval, quantified promo lift (%), and a note on forecast reliability/limitations for the CFO's planning use case.
