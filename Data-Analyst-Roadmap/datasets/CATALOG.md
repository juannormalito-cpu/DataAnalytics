# Dataset Catalog

Master index of every dataset referenced across the handbook, organized by chapter. Each entry: **Difficulty · Description · Business Context · Skills Learned · Expected Deliverables · Questions to Answer · Estimated Time · Link**. See also the per-dataset brief in [`03_Databases/adventure_works.md`](03_Databases/adventure_works.md) and the [Notion Dataset Database](../notion/06_Dataset_Database.md).

---

## Chapter 03 — Databases
### Adventure Works *(full brief: [03_Databases/adventure_works.md](03_Databases/adventure_works.md))*
Beginner–Intermediate · Microsoft's sample OLTP DB for a bicycle manufacturer. **Link:** kaggle.com/datasets/ukveteran/adventure-works

### Northwind
- **Difficulty:** Beginner
- **Description:** Classic small-business OLTP sample (customers, orders, products, suppliers, employees).
- **Business Context:** The textbook example for practicing PK/FK relationships and normalization before moving to a larger schema.
- **Skills Learned:** Multi-table JOINs, aggregate queries, basic schema reading.
- **Expected Deliverables:** SQL answering top-customer and top-product questions; an ERD.
- **Questions to Answer:** Which employees generate the most revenue? Which suppliers have the slowest fulfillment?
- **Estimated Time:** 3–4 hours
- **Link:** https://www.kaggle.com/datasets/mahoora00135/northwind

---

## Chapter 04 — SQL
### Global Superstore
- **Difficulty:** Beginner
- **Description:** Retail orders across regions, product categories, and customer segments.
- **Business Context:** The go-to dataset for practicing `GROUP BY`, `JOIN`, and window functions on a realistic retail schema.
- **Skills Learned:** Aggregation, ranking, running totals, period-over-period comparisons.
- **Expected Deliverables:** A SQL notebook answering 10 business questions with window functions.
- **Questions to Answer:** Which region has the best profit margin? What's the month-over-month sales trend by category?
- **Estimated Time:** 4–5 hours
- **Link:** https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset

### European Soccer Database
- **Difficulty:** Intermediate
- **Description:** Matches, players, teams, and leagues across European soccer, 2008–2016.
- **Business Context:** A large, deeply relational schema good for practicing complex multi-table joins and subqueries.
- **Skills Learned:** Deep joins, CTEs, subqueries, window functions for rankings.
- **Expected Deliverables:** SQL identifying top-performing teams/players by custom criteria.
- **Questions to Answer:** Which teams most improved season-over-season? Which players' stats best predict match outcomes?
- **Estimated Time:** 5–7 hours
- **Link:** https://www.kaggle.com/datasets/hugomathien/soccer

---

## Chapter 05 — Python
### Titanic
- **Difficulty:** Beginner
- **Description:** Passenger manifest with survival outcome.
- **Business Context:** The standard first dataset for cleaning, EDA, and basic feature engineering.
- **Skills Learned:** Missing-value handling, categorical encoding, EDA visualization.
- **Expected Deliverables:** A cleaned dataset + EDA notebook with 5+ charts and written findings.
- **Questions to Answer:** What factors most correlate with survival?
- **Estimated Time:** 2–3 hours
- **Link:** https://www.kaggle.com/competitions/titanic

### House Prices
- **Difficulty:** Beginner–Intermediate
- **Description:** Residential home sale prices with ~80 explanatory features.
- **Business Context:** Practicing feature engineering and handling many messy, mixed-type columns.
- **Skills Learned:** Missing data strategy, encoding, correlation analysis, feature engineering.
- **Expected Deliverables:** A cleaned, feature-engineered dataset ready for modeling.
- **Questions to Answer:** Which features most drive sale price? Are there regional/seasonal effects?
- **Estimated Time:** 4–6 hours
- **Link:** https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques

### Instacart Market Basket
- **Difficulty:** Intermediate
- **Description:** Millions of grocery orders with product/aisle/department detail.
- **Business Context:** Practicing feature engineering at scale and basket-level aggregation with Pandas.
- **Skills Learned:** Groupby aggregation at scale, merge strategy, memory-efficient Pandas.
- **Expected Deliverables:** Customer-level feature table (order frequency, basket size, reorder rate).
- **Questions to Answer:** What predicts whether a product gets reordered?
- **Estimated Time:** 5–7 hours
- **Link:** https://www.kaggle.com/competitions/instacart-market-basket-analysis

---

## Chapter 06 — Power BI
### Global Superstore *(reused — see Chapter 04)*
Also the standard first Power BI dashboard build: sales/profit KPIs, region drill-through, product category breakdown.

### Google Play Store Apps
- **Difficulty:** Beginner
- **Description:** App metadata — category, rating, installs, price, reviews.
- **Business Context:** Practicing Power Query cleaning (messy install counts, price strings) before modeling.
- **Skills Learned:** Power Query transformation, categorical DAX measures, KPI cards.
- **Expected Deliverables:** A published dashboard: top categories by installs, rating distribution, free vs. paid comparison.
- **Questions to Answer:** Which app categories have the best rating-to-install ratio?
- **Estimated Time:** 4–5 hours
- **Link:** https://www.kaggle.com/datasets/lava18/google-play-store-apps

---

## Chapter 07 — Professional Projects
See [`../projects/`](../projects/) — each of the 10 projects has its own dataset assigned in its README, drawn from this catalog plus:

### Customer Churn (Telco)
Intermediate · Classic churn dataset (contract type, tenure, charges, churn flag). **Link:** kaggle.com/datasets/blastchar/telco-customer-churn — used in [Project 02](../projects/02_Ecommerce_Customer_Churn/).

### Rossmann Store Sales
Intermediate · Daily sales across 1,000+ drug stores with promo/holiday flags. **Link:** kaggle.com/c/rossmann-store-sales — relevant to [Project 08 (Financial Forecasting)](../projects/08_Financial_Forecasting/).

---

## Chapter 08 — Machine Learning
### Credit Card Fraud Detection
- **Difficulty:** Advanced
- **Description:** ~285k anonymized European card transactions, ~0.17% fraud.
- **Business Context:** The canonical extreme-class-imbalance classification problem — see [08.4](../handbook/08_Machine_Learning.md#84-model-evaluation).
- **Skills Learned:** Imbalanced classification, precision/recall trade-offs, resampling (SMOTE), threshold tuning.
- **Expected Deliverables:** A cross-validated classifier with a precision/recall analysis and a recommended decision threshold.
- **Questions to Answer:** What's the optimal precision/recall trade-off given a business cost for false positives vs. false negatives?
- **Estimated Time:** 8–10 hours
- **Link:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud — used in [Project 05](../projects/05_Credit_Card_Fraud_Detection/).

### Steam Games / Spotify Tracks
Intermediate–Advanced · Content + usage metadata, good for recommendation-system practice. **Links:** kaggle.com/datasets/fronkongames/steam-games-dataset · kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset — relevant to [Project 09 (Recommendation Engine)](../projects/09_Product_Recommendation_Engine/).

### Formula 1 World Championship
Intermediate · Race results, lap times, driver/constructor standings 1950–present. Good for time-series and ranking practice. **Link:** kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020

---

## Chapter 09 — Portfolio & Career
### Airbnb Listings, Netflix Titles, Amazon Reviews
Beginner–Intermediate · Popular, recognizable datasets for building a diverse, story-driven portfolio piece a recruiter will actually open. **Links:** insideairbnb.com · kaggle.com/datasets/shivamb/netflix-shows · kaggle.com/datasets/snap/amazon-fine-food-reviews — good raw material for the [Chapter 07 methodology](../handbook/07_Professional_Projects.md) applied to a dataset of your own choosing beyond the 10 assigned projects.
