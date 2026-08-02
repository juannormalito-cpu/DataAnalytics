# Project 03 · Adventure Works BI

**Difficulty:** Intermediate · **Stack:** SQL, Power BI · **Dataset:** [Adventure Works](../../datasets/03_Databases/adventure_works.md)

## Business Problem
CFO: *"We have a normalized OLTP database and no reporting layer. I need a real BI system — sales, production costs, and sales-territory performance — built on top of it."*

## Objectives
- Remodel the normalized OLTP schema into a Star Schema.
- Build a warehouse-style reporting layer with SQL views.
- Ship a multi-page executive dashboard.

## Database Diagram
Source: normalized Adventure Works OLTP schema. Target: `fact_sales` + `dim_product`, `dim_customer`, `dim_date`, `dim_territory` — the exact remodeling exercise from [Chapter 03.3](../../handbook/03_Databases.md#33-star-schema-vs-snowflake-schema).

## Questions to Answer
1. Which sales territories are growing vs. shrinking year over year?
2. Which product categories have the healthiest margins after production cost?
3. Which sales reps are outperforming their territory average?
4. What's the seasonality pattern in bicycle sales?

## Workflow
- **SQL** ([`sql/`](sql/)): the OLTP → Star Schema transformation script (views per [Chapter 04.5](../../handbook/04_SQL.md#45-views--stored-procedures)).
- **Power BI** ([`powerbi/`](powerbi/)): full data model + DAX for YoY growth, margin %, rep performance vs. territory average.
- **Diagrams** ([`diagrams/`](diagrams/)): before (OLTP ERD) / after (Star Schema) comparison.

## Expected Dashboard
Executive overview + territory drill-through + rep leaderboard + seasonality trend page.

## Expected Conclusions
A ranked territory growth report, a margin-by-category breakdown, and a recommendation on which underperforming territories need investigation.
