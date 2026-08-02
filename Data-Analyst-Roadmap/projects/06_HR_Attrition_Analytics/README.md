# Project 06 · HR Attrition Analytics

**Difficulty:** Intermediate · **Stack:** SQL, Python, Power BI · **Dataset:** IBM HR Analytics Employee Attrition (Kaggle)

## Business Problem
Head of People: *"Attrition is up and it's expensive to replace people. I want to know which departments and roles are highest-risk and why, before I present this to the executive team."*

## Objectives
- Quantify attrition rate by department, role, and tenure.
- Identify the strongest predictors of attrition.
- Build an HR-facing dashboard plus a predictive risk list.

## Database Diagram
`fact_employee_snapshot` (employee_id, department, role, tenure, satisfaction_score, salary, attrition_flag) — a single wide table typical of HR datasets; modeled lightly per [Chapter 03](../../handbook/03_Databases.md).

## Questions to Answer
1. Which departments/roles have the highest attrition rate?
2. Does compensation or job satisfaction correlate more strongly with attrition?
3. Is there a tenure "danger zone" (e.g., 1–2 years) where attrition spikes?
4. Can we predict which current employees are at highest risk of leaving?

## Workflow
- **SQL** ([`sql/`](sql/)): attrition rate by segment, tenure cohort analysis.
- **Python** ([`python/`](python/)): EDA + a classification model for attrition risk ([Chapter 08](../../handbook/08_Machine_Learning.md)).
- **Power BI** ([`powerbi/`](powerbi/)): HR dashboard with department drill-through and a risk-flagged employee table.

## Expected Dashboard
Attrition KPI overview, department/role breakdown, tenure danger-zone chart, at-risk employee table.

## Expected Conclusions
Top 3 attrition drivers ranked by model importance, and a targeted retention recommendation (e.g., "compensation review for mid-tenure engineers").
