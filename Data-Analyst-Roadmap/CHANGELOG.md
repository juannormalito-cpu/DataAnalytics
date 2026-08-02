# Changelog

All notable progress on this handbook is tracked here, newest first. Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## 2026-07-31 — Spanish translation
### Added
- [`handbook_es/`](handbook_es/) — full Spanish translation of all 9 chapters plus [`00_Tabla_de_Contenidos.md`](handbook_es/00_Tabla_de_Contenidos.md), code/SQL/DAX kept as-is, prose and diagram labels translated.
- [pdf/build_pdf.py](pdf/build_pdf.py) — extended with `--lang es` to build from `/handbook_es`.
- [pdf/El_Roadmap_Completo_del_Analista_de_Datos.pdf](pdf/El_Roadmap_Completo_del_Analista_de_Datos.pdf) — compiled Spanish PDF (cover, ToC, headers/footers).
### Next up
- Per-chapter exercise sets, per-project SQL/Python/Power BI artifacts (both languages).

## 2026-07-31 — Datasets, projects, PDF, and Notion automation
### Added
- [datasets/CATALOG.md](datasets/CATALOG.md) — full dataset catalog organized by chapter (Adventure Works, Northwind, Titanic, House Prices, Global Superstore, Instacart, Google Play Store, Customer Churn, Rossmann, Credit Card Fraud, Steam, Spotify, Formula 1, Airbnb, Netflix, Amazon Reviews) plus [datasets/03_Databases/adventure_works.md](datasets/03_Databases/adventure_works.md).
- All 10 project READMEs in [`projects/`](projects/) — each with Business Problem, Database Diagram, Objectives, Questions to Answer, Workflow (SQL/Python/Power BI), Expected Dashboard, Expected Conclusions, per the [Chapter 07 methodology](handbook/07_Professional_Projects.md).
- [pdf/build_pdf.py](pdf/build_pdf.py) — build script that compiles all 9 chapters into a styled, printable document (cover, ToC, running headers/footers). Rendered via headless Microsoft Edge to [pdf/The_Complete_Data_Analyst_Roadmap.pdf](pdf/The_Complete_Data_Analyst_Roadmap.pdf).
- [notion/build_notion_workspace.py](notion/build_notion_workspace.py) — Notion API script that auto-creates the full workspace hierarchy and content from the `/notion` Markdown files.
- [notion/NOTION_AI_PROMPT.md](notion/NOTION_AI_PROMPT.md) — copy-paste prompt for Notion AI to scaffold the same hierarchy without API setup, for users who prefer the manual route.
### Updated
- Marked datasets, all 10 projects, and the PDF ✅ in [progress/PROGRESS.md](progress/PROGRESS.md) and [notion/02_Progress_Tracker.md](notion/02_Progress_Tracker.md); [notion/05_Project_Database.md](notion/05_Project_Database.md) marked all projects ✅.
- [README.md](README.md) status line, PDF build instructions, and Notion import instructions.
### Remaining
- Per-chapter exercise sets (`exercises/`) — warm-up/practice/challenge/mini-project/solutions content.
- Per-project executable SQL/Python/Power BI artifacts (currently scoped in each project README; code/dashboards not yet built).

## 2026-07-31 — Chapters 02–09: full handbook core complete
### Added
- [handbook/02_How_Companies_Work.md](handbook/02_How_Companies_Work.md) — data generation, OLTP→ETL/ELT→Warehouse, Warehouse vs. Lake vs. Lakehouse, batch vs. streaming, AWS/Azure/GCP, full pipeline diagram.
- [handbook/03_Databases.md](handbook/03_Databases.md) — PK/FK/indexes, normalization (1NF-3NF), Star vs. Snowflake schema, OLTP vs. OLAP, ERD diagrams, SQL preview.
- [handbook/04_SQL.md](handbook/04_SQL.md) — complete SQL course: SELECT/WHERE/ORDER BY, GROUP BY/HAVING, JOIN/UNION, CTEs/subqueries, Views/Stored Procedures, window functions/ranking, performance/indexing — each with business case, example, and exercise+solution.
- [handbook/05_Python.md](handbook/05_Python.md) — Pandas/NumPy, cleaning, EDA, feature engineering, visualization/stats, project structure/venv/logging.
- [handbook/06_Power_BI.md](handbook/06_Power_BI.md) — Power Query, star-schema modeling, DAX/measures/KPIs, dashboards/bookmarks/drill-through, deployment best practices.
- [handbook/07_Professional_Projects.md](handbook/07_Professional_Projects.md) — 7-step project methodology; indexes the 10 portfolio projects.
- [handbook/08_Machine_Learning.md](handbook/08_Machine_Learning.md) — regression/classification/clustering/recsys/time series/NLP, pipelines/cross-validation, evaluation metrics, hyperparameter tuning, deployment/drift.
- [handbook/09_Portfolio_Career.md](handbook/09_Portfolio_Career.md) — Git/GitHub, README, resume formula, interview question bank, freelancing, learning timelines.
### Updated
- All 9 chapters marked ✅ in [handbook/00_Table_of_Contents.md](handbook/00_Table_of_Contents.md), [notion/01_Chapter_Index.md](notion/01_Chapter_Index.md), [notion/02_Progress_Tracker.md](notion/02_Progress_Tracker.md), [progress/PROGRESS.md](progress/PROGRESS.md).
### Next up
- Datasets catalog, 10 portfolio projects, printable PDF, Notion workspace automation.

## 2026-07-31 — Chapter 01: Introduction
### Added
- [handbook/01_Introduction.md](handbook/01_Introduction.md) — production-ready: what is data, the six roles compared (BI Analyst, Data Analyst, Data Scientist, Data Engineer, Analytics Engineer, ML Engineer), daily responsibilities per role, career path diagram, salary benchmarks (LatAm/US/EU), skills matrix, recommended books & YouTube channels. Includes 2 Mermaid diagrams and real-company examples (Spotify, Mercado Libre).
### Updated
- Marked Chapter 01 ✅ in [handbook/00_Table_of_Contents.md](handbook/00_Table_of_Contents.md), [notion/01_Chapter_Index.md](notion/01_Chapter_Index.md), [notion/02_Progress_Tracker.md](notion/02_Progress_Tracker.md), and [progress/PROGRESS.md](progress/PROGRESS.md).
### Next up
- Chapter 02 — How Companies Work.

## 2026-07-31 — Repository scaffold
### Added
- Full repository directory structure: `handbook/`, `notion/`, `exercises/`, `datasets/`, `projects/`, `assets/`, `references/`, `pdf/`, `progress/`.
- Per-chapter subfolders in `exercises/` (`warmup/practice/challenge/mini_project/solutions`) and `datasets/` for all 9 chapters.
- Per-project subfolders in `projects/` (`data/sql/python/powerbi/diagrams/presentation`) for all 10 planned portfolio projects.
- [handbook/00_Table_of_Contents.md](handbook/00_Table_of_Contents.md) — master table of contents linking all 9 parts.
- Notion workspace hierarchy (10 pages): Home, Chapter Index, Progress Tracker, Checklist, Learning Calendar, Project Database, Dataset Database, Exercise Database, Interview Tracker, Resources.
- [README.md](README.md), this CHANGELOG, and [progress/PROGRESS.md](progress/PROGRESS.md).

### Next up
- Chapter 01 — Introduction.
