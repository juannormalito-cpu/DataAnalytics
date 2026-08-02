# Project 10 · Capstone: End-to-End Pipeline

**Difficulty:** Advanced · **Stack:** SQL, Python, Power BI, ML · **Dataset:** Your choice, or combine [Global Superstore](../../datasets/CATALOG.md#chapter-04--sql) + [Customer Churn](../../datasets/CATALOG.md#chapter-07--professional-projects)

## Business Problem
This is the synthesis project: pick (or reuse) a business problem and take it through the **entire pipeline** from [Chapter 02](../../handbook/02_How_Companies_Work.md) — raw data all the way to a deployed prediction — demonstrating every skill in this handbook in one cohesive project.

## Objectives
- Model a proper Star Schema warehouse from raw source data.
- Build the SQL transformation layer.
- Perform Python EDA/feature engineering and train a model.
- Ship a Power BI dashboard that includes the model's output.
- Wrap the trained model in a minimal API (per [Chapter 08.6](../../handbook/08_Machine_Learning.md#86-deployment-the-ml-engineer-handoff)).

## Database Diagram
Full pipeline: raw source → OLTP-style staging → `fact`/`dim` warehouse tables → model feature table — the complete diagram from [Chapter 02.6](../../handbook/02_How_Companies_Work.md#26-the-full-picture).

## Questions to Answer
1. What's the business question this capstone answers, end to end?
2. What does the warehouse schema look like, and why did you model it that way?
3. What did EDA and feature engineering reveal that shaped the model?
4. How does the deployed prediction actually change what the business does?

## Workflow
- **SQL** ([`sql/`](sql/)): warehouse schema + transformation views.
- **Python** ([`python/`](python/)): EDA, feature engineering, model training + a lightweight API wrapper (FastAPI/Flask).
- **Power BI** ([`powerbi/`](powerbi/)): dashboard combining descriptive analytics and model output (e.g., risk scores) in one view.
- **Presentation** ([`presentation/`](presentation/)): a full executive summary treating this as a real company initiative — problem, approach, results, what you'd do with more time/data.

## Expected Dashboard
A single dashboard combining historical analytics (from the warehouse) with forward-looking predictions (from the model) — the complete Business Decision + Machine Learning loop from [Chapter 02.6](../../handbook/02_How_Companies_Work.md#26-the-full-picture).

## Expected Conclusions
A complete narrative: business problem → data pipeline → model → decision → recommended next steps if this were shipped to production, written as your capstone portfolio centerpiece.
