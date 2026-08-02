# Project 07 · Marketing Campaign Performance

**Difficulty:** Intermediate · **Stack:** SQL, Power BI · **Dataset:** Marketing Campaign Performance (Kaggle) or client campaign export

## Business Problem
CMO: *"We run campaigns across five channels and I can't tell which ones are actually driving revenue versus just spend."*

## Objectives
- Build a unified campaign performance view across channels.
- Calculate ROAS (Return on Ad Spend) and CAC (Customer Acquisition Cost) per channel/campaign.
- Recommend budget reallocation.

## Database Diagram
`fact_campaign_events` (campaign_id, channel_id, date_id, spend, impressions, clicks, conversions, revenue) with `dim_channel`, `dim_campaign`, `dim_date` — Star Schema per [Chapter 03](../../handbook/03_Databases.md).

## Questions to Answer
1. Which channels have the best ROAS and CAC?
2. How does performance trend over the campaign lifecycle (early vs. late)?
3. Are there diminishing returns visible as spend increases on a channel?
4. Which campaigns should be scaled up, and which should be cut?

## Workflow
- **SQL** ([`sql/`](sql/)): ROAS/CAC calculations, spend-vs-conversion trend queries with window functions ([Chapter 04](../../handbook/04_SQL.md)).
- **Power BI** ([`powerbi/`](powerbi/)): channel comparison dashboard with ROAS/CAC as headline DAX measures ([Chapter 06](../../handbook/06_Power_BI.md)).

## Expected Dashboard
Channel comparison overview, campaign-level drill-through, spend-vs-return scatter view.

## Expected Conclusions
A ranked channel list by ROAS, a specific reallocation recommendation (e.g., "shift 20% of Channel X spend to Channel Y"), and flagged campaigns showing diminishing returns.
