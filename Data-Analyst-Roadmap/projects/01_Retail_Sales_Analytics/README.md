# Project 01 · Retail Sales Analytics

**Difficulty:** Beginner · **Stack:** SQL, Power BI · **Dataset:** [Global Superstore](../../datasets/CATALOG.md#chapter-04--sql)

## Business Problem
Regional VP of Sales: *"I don't trust the numbers different regional managers are reporting to me — I want one dashboard that tells me the truth about sales and profit, by region and category, without anyone's spin."*

## Objectives
- Build a single source of truth for revenue, profit, and order volume.
- Identify underperforming regions/categories and quantify the gap.
- Ship a self-serve dashboard so the VP stops needing ad-hoc reports.

## Database Diagram
Star schema: `fact_orders` (order_id, date_id, customer_id, product_id, region_id, sales, profit, quantity) with `dim_date`, `dim_customer`, `dim_product`, `dim_region` — see [Chapter 03](../../handbook/03_Databases.md) for the modeling pattern.

## Questions to Answer
1. Which regions/categories drive the most profit — and the most loss?
2. What's the month-over-month sales trend, and is it seasonal or declining?
3. Which product sub-categories have negative margin despite high sales volume?
4. Which customer segment is most profitable per order?

## Workflow
- **SQL** ([`sql/`](sql/)): build `fact_orders` + dimensions; write the 4 core aggregation queries answering the questions above ([Chapter 04](../../handbook/04_SQL.md) patterns: `GROUP BY`/`HAVING`, window functions for MoM trend).
- **Power BI** ([`powerbi/`](powerbi/)): star-schema model, DAX measures for `Total Sales`, `Total Profit`, `Profit Margin %`, `Sales MoM %` ([Chapter 06](../../handbook/06_Power_BI.md)).
- **Presentation** ([`presentation/`](presentation/)): 1-page executive summary with the top 3 findings and a recommendation.

## Expected Dashboard
A 3-page report: (1) Executive KPI overview, (2) Region/Category drill-through, (3) Trend over time with a target line.

## Expected Conclusions
A ranked list of underperforming category × region combinations with a quantified profit-recovery estimate, plus a recommendation on where to reallocate marketing spend.
