# Project 05 · Credit Card Fraud Detection

**Difficulty:** Advanced · **Stack:** Python, ML · **Dataset:** [Credit Card Fraud](../../datasets/CATALOG.md#chapter-08--machine-learning)

## Business Problem
Head of Risk: *"We block too many legitimate transactions and miss too much real fraud. I need a model that finds the right trade-off, and I need to understand what that trade-off costs us."*

## Objectives
- Build a classifier for an extremely imbalanced fraud dataset (~0.17% positive).
- Choose and justify an evaluation metric appropriate to class imbalance.
- Recommend a decision threshold based on estimated business cost of false positives vs. false negatives.

## Database Diagram
Single flat transaction table (anonymized PCA features + `Amount`, `Time`, `Class`) — no warehouse modeling needed here; the focus is entirely [Chapter 08](../../handbook/08_Machine_Learning.md).

## Questions to Answer
1. What's the baseline fraud rate, and why is accuracy the wrong metric here?
2. Which model (logistic regression, random forest, gradient boosting) gives the best precision/recall trade-off?
3. What decision threshold minimizes estimated business cost?
4. How stable is the model's performance across cross-validation folds?

## Workflow
- **Python** ([`python/`](python/)): EDA, class-imbalance handling (class weighting or SMOTE), a `Pipeline` + `GridSearchCV` per [Chapter 08.3–08.5](../../handbook/08_Machine_Learning.md#83-pipelines--cross-validation), evaluated on precision/recall/F1/ROC-AUC.
- **Presentation** ([`presentation/`](presentation/)): a threshold-selection chart (precision vs. recall vs. threshold) translated into an estimated $ cost curve for a non-technical Risk audience.

## Expected Dashboard
N/A (Python-only project) — deliverable is a model evaluation report with a recommended threshold.

## Expected Conclusions
A recommended model + threshold, with an explicit statement of the precision/recall trade-off in business terms (e.g., "at this threshold we catch 92% of fraud while flagging 0.4% of legitimate transactions for review").
