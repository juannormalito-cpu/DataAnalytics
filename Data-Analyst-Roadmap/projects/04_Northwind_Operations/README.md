# Project 04 · Northwind Operations

**Difficulty:** Beginner · **Stack:** SQL · **Dataset:** [Northwind](../../datasets/CATALOG.md#chapter-03--databases)

## Business Problem
Operations Manager: *"Are we shipping orders fast enough, and which suppliers are causing delays?"*

## Objectives
- Measure order-to-ship time and identify bottlenecks.
- Rank suppliers and employees by operational performance.
- Deliver a clean SQL report Operations can rerun weekly.

## Database Diagram
Classic Northwind OLTP schema: `orders`, `order_details`, `products`, `suppliers`, `employees`, `customers` — practiced in [Chapter 03](../../handbook/03_Databases.md).

## Questions to Answer
1. What's the average and 90th-percentile order-to-ship time?
2. Which suppliers are associated with the slowest-shipping products?
3. Which employees process the most orders, and how does their average shipping time compare?
4. Are there seasonal spikes in order volume that strain fulfillment?

## Workflow
- **SQL** ([`sql/`](sql/)): the entire deliverable — joins, `GROUP BY`/`HAVING`, and window functions for percentile/ranking questions ([Chapter 04](../../handbook/04_SQL.md)).

## Expected Dashboard
N/A — this project intentionally stays SQL-only to build pure query fluency; output is a set of ranked result tables and a written report.

## Expected Conclusions
A ranked list of suppliers correlated with shipping delays and a recommendation on which supplier relationships to review.
