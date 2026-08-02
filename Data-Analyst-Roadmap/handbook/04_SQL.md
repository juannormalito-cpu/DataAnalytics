# 04 · SQL — The Complete Course

*Part 4 of [The Complete Data Analyst & Data Science Roadmap](00_Table_of_Contents.md) · Previous: [03. Databases](03_Databases.md)*

> 💡 **What you'll be able to do after this chapter**
> Write real analytical SQL end to end — filtering, aggregating, joining, windowing, and optimizing — against the Star Schema from [Chapter 03](03_Databases.md). This is the single highest-leverage skill in the whole handbook.

All examples use the `fact_sales` / `dim_product` / `dim_customer` / `dim_date` / `dim_store` schema introduced in [03.3](03_Databases.md#33-star-schema-vs-snowflake-schema). Solutions for every exercise live in [`../exercises/04_SQL/solutions/`](../exercises/04_SQL/solutions/).

---

## 4.1 SELECT, WHERE, ORDER BY

```sql
SELECT product_name, category, price
FROM dim_product
WHERE category = 'Electronics'
ORDER BY price DESC;
```

> 🏢 **Business case:** Marketing asks for "every Electronics product priced above $50, most expensive first" to plan a promo.

**Exercise:** List all customers who signed up in 2025, ordered by signup date.
<details><summary>Solution</summary>

```sql
SELECT customer_id, name, signup_date
FROM dim_customer
WHERE signup_date >= '2025-01-01' AND signup_date < '2026-01-01'
ORDER BY signup_date;
```
</details>

---

## 4.2 GROUP BY, HAVING

`GROUP BY` collapses rows into groups; `HAVING` filters *after* aggregation (`WHERE` filters *before*).

```sql
SELECT category, SUM(revenue) AS total_revenue
FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id
GROUP BY category
HAVING SUM(revenue) > 100000;
```

> 🏢 **Business case:** Finance wants only categories that generated over $100k — small categories are noise for this review.

**Exercise:** Find stores with more than 500 total orders.
<details><summary>Solution</summary>

```sql
SELECT store_id, COUNT(*) AS order_count
FROM fact_sales
GROUP BY store_id
HAVING COUNT(*) > 500;
```
</details>

---

## 4.3 JOIN, UNION

| JOIN type | Returns |
|---|---|
| `INNER JOIN` | Only rows matching in both tables |
| `LEFT JOIN` | All rows from the left table, matched rows from the right (NULL if no match) |
| `RIGHT JOIN` | Mirror of LEFT JOIN |
| `FULL OUTER JOIN` | All rows from both, matched where possible |

```sql
-- Customers with no orders yet (classic LEFT JOIN use case)
SELECT c.customer_id, c.name
FROM dim_customer c
LEFT JOIN fact_sales f ON c.customer_id = f.customer_id
WHERE f.customer_id IS NULL;
```

`UNION` stacks result sets vertically (and removes duplicates; `UNION ALL` keeps them — and is faster).

> 🏢 **Business case:** Growth wants a "never purchased" list for a first-order discount campaign — exactly the `LEFT JOIN ... WHERE ... IS NULL` pattern above.

**Exercise:** Combine a list of online orders and in-store orders into one result set, keeping duplicates.
<details><summary>Solution</summary>

```sql
SELECT order_id, 'online' AS channel FROM online_orders
UNION ALL
SELECT order_id, 'in_store' AS channel FROM instore_orders;
```
</details>

---

## 4.4 CTEs & Subqueries

A **CTE** (Common Table Expression, `WITH`) names a subquery so you can build a query in readable steps.

```sql
WITH monthly_revenue AS (
    SELECT DATE_TRUNC('month', d.full_date) AS month, SUM(f.revenue) AS revenue
    FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY 1
)
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS mom_change
FROM monthly_revenue
ORDER BY month;
```

> ✅ **Best practice**
> Prefer CTEs over deeply nested subqueries — they read top-to-bottom like a narrative, and every analyst on your team can debug them piece by piece.

**Exercise:** Find the top-spending customer per region using a CTE.
<details><summary>Solution</summary>

```sql
WITH customer_totals AS (
    SELECT c.region, c.customer_id, SUM(f.revenue) AS total_spent
    FROM fact_sales f JOIN dim_customer c ON f.customer_id = c.customer_id
    GROUP BY c.region, c.customer_id
),
ranked AS (
    SELECT *, RANK() OVER (PARTITION BY region ORDER BY total_spent DESC) AS rnk
    FROM customer_totals
)
SELECT region, customer_id, total_spent
FROM ranked
WHERE rnk = 1;
```
</details>

---

## 4.5 Views & Stored Procedures

- **View:** a saved query you can `SELECT` from like a table — great for hiding complexity from other analysts.
- **Stored Procedure:** a saved, parameterized block of SQL (and logic) you `CALL` — used more by engineers than analysts, but you should recognize one when you see it.

```sql
CREATE VIEW vw_monthly_category_revenue AS
SELECT DATE_TRUNC('month', d.full_date) AS month, p.category, SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY 1, 2;
```

> 🏢 **Business case:** Instead of every analyst re-writing the same 3-table join every week for the exec dashboard, an **Analytics Engineer** exposes it as a view — this is the "single source of truth" idea from [01.2](01_Introduction.md).

---

## 4.6 Window Functions & Ranking

Window functions compute across a set of rows *related to the current row*, without collapsing them like `GROUP BY` does.

| Function | Use |
|---|---|
| `ROW_NUMBER()` | Unique sequential number per row |
| `RANK()` / `DENSE_RANK()` | Ranking with (`RANK`) or without (`DENSE_RANK`) gaps on ties |
| `LAG()` / `LEAD()` | Value from a previous/next row |
| `SUM()/AVG() OVER (...)` | Running totals, moving averages |

```sql
SELECT
    customer_id, order_date, revenue,
    SUM(revenue) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM fact_sales;
```

> 🏢 **Business case:** "Show me each customer's cumulative lifetime spend over time" — the classic running-total window function question, and one of the most common SQL interview questions.

**Exercise:** For each product, rank its sales by revenue within its category.
<details><summary>Solution</summary>

```sql
SELECT
    p.category, p.product_name, f.revenue,
    DENSE_RANK() OVER (PARTITION BY p.category ORDER BY f.revenue DESC) AS rank_in_category
FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id;
```
</details>

---

## 4.7 Performance, Indexes & Optimization

> ⚠️ **Common mistakes**
> - `SELECT *` on a wide warehouse table when you need 3 columns — reads far more data than necessary.
> - Filtering on a function applied to a column (`WHERE YEAR(order_date) = 2026`) — this often prevents the database from using an index. Prefer `WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01'`.
> - Joining on unindexed columns for large tables — check with your Data Engineer if a hot join path is slow.

> ✅ **Best practices**
> - Filter as early as possible (`WHERE` before `JOIN`ing more tables than necessary).
> - Read the query's **execution plan** (`EXPLAIN` / `EXPLAIN ANALYZE`) when a query is unexpectedly slow — it tells you whether it's scanning a full table or using an index.
> - Aggregate at the coarsest level the question actually needs — don't pull row-level data into Python just to sum it there.

---

## Chapter Summary

- `SELECT/WHERE/ORDER BY` → `GROUP BY/HAVING` → `JOIN` are the daily-driver 80% of analyst SQL.
- CTEs make multi-step logic readable; Views expose that logic as reusable, trusted building blocks.
- Window functions solve "compare this row to other rows" problems without collapsing your result set — rankings, running totals, period-over-period change.
- Query performance is mostly about filtering early, avoiding functions on filtered columns, and reading the execution plan when something's slow.

Full exercise sets (warm-up → challenge → mini project) live in [`../exercises/04_SQL/`](../exercises/04_SQL/).

**Next:** [05. Python →](05_Python.md) — where SQL output becomes cleaning, EDA, and feature engineering.
