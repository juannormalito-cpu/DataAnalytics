-- Quick sanity check after `python main.py` loads the Star Schema.
SELECT 'dim_time' AS tabla, COUNT(*) FROM dim_time
UNION ALL SELECT 'dim_type', COUNT(*) FROM dim_type
UNION ALL SELECT 'fact_transactions', COUNT(*) FROM fact_transactions;
