# Project 02 · E-commerce Customer Churn

**Difficulty:** Intermediate · **Stack:** SQL, Python · **Dataset:** [Telco Customer Churn](../../datasets/CATALOG.md#chapter-07--professional-projects)

## Business Problem
Head of Retention: *"We're losing customers and I don't know why until they're already gone. I need to know who's at risk before they churn, and what's actually driving it."*

## Objectives
- Quantify churn rate and its trend.
- Identify the strongest drivers of churn.
- Produce a scored, ranked list of at-risk customers Retention can act on.

## Database Diagram
`fact_subscriptions` (customer_id, tenure_months, monthly_charges, contract_type, churn_flag) joined to `dim_customer` — a flatter schema typical of a churn dataset, per [Chapter 03](../../handbook/03_Databases.md).

## Questions to Answer
1. What is the overall churn rate, and how does it vary by contract type and tenure?
2. Which features correlate most strongly with churn?
3. Can we build a model that reliably flags at-risk customers before they leave?
4. What's the estimated revenue at risk from the top decile of at-risk customers?

## Workflow
- **SQL** ([`sql/`](sql/)): churn rate by segment, cohort retention curves ([Chapter 04](../../handbook/04_SQL.md) window functions).
- **Python** ([`python/`](python/)): EDA + feature engineering + a classification pipeline with cross-validation ([Chapter 05](../../handbook/05_Python.md), [Chapter 08](../../handbook/08_Machine_Learning.md)) — evaluated on **precision/recall**, not accuracy, given class imbalance.
- **Power BI** ([`powerbi/`](powerbi/)): a retention dashboard with a risk-score table exported from the Python model.

## Expected Dashboard
Churn KPI overview + a sortable table of at-risk customers with predicted churn probability, for Retention to action directly.

## Expected Conclusions
The top 3 churn drivers (e.g., month-to-month contracts, low tenure, high monthly charges), a model precision/recall trade-off recommendation, and an estimated revenue-at-risk figure.
