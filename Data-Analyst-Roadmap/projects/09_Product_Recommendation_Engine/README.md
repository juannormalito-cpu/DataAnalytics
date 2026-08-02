# Project 09 · Product Recommendation Engine

**Difficulty:** Advanced · **Stack:** Python, ML · **Dataset:** [Steam Games / Spotify Tracks](../../datasets/CATALOG.md#chapter-08--machine-learning)

## Business Problem
Head of Product: *"Users browse but don't discover — we want 'you might also like' recommendations that actually increase engagement."*

## Objectives
- Build a recommendation system from user interaction data.
- Compare collaborative filtering vs. content-based approaches.
- Evaluate recommendation quality with an appropriate offline metric.

## Database Diagram
`fact_interactions` (user_id, item_id, interaction_type, timestamp) with `dim_item` (genre/category/metadata) — per [Chapter 03](../../handbook/03_Databases.md).

## Questions to Answer
1. How sparse is the user-item interaction matrix, and what does that imply for approach choice?
2. Does collaborative filtering or content-based filtering perform better for this dataset?
3. How do we evaluate "good recommendations" offline (precision@k, recall@k) before any live test?
4. What's the cold-start plan for new users/items?

## Workflow
- **Python** ([`python/`](python/)): build both a content-based (similarity on item metadata) and collaborative-filtering (matrix factorization) recommender, evaluate with precision@k/recall@k, per [Chapter 08.1](../../handbook/08_Machine_Learning.md#81-the-problem-types).
- **Presentation** ([`presentation/`](presentation/)): a comparison table of approaches and a recommended production approach, including the cold-start plan.

## Expected Dashboard
N/A (Python-only) — deliverable is an evaluation report + example recommendation outputs for sample users.

## Expected Conclusions
A recommended approach (content-based, collaborative, or hybrid) with supporting offline metrics, and a cold-start strategy for new users/items.
