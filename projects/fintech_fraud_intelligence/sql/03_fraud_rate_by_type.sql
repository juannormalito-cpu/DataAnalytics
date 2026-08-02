-- Tasa de fraude por tipo de transacción — PaySim solo tiene fraude real en
-- TRANSFER y CASH_OUT, pero conviene verlo con datos, no asumirlo.
SELECT
    t.type,
    COUNT(*)                                   AS total_transacciones,
    SUM(CASE WHEN f.is_fraud THEN 1 ELSE 0 END) AS transacciones_fraudulentas,
    ROUND(
        100.0 * SUM(CASE WHEN f.is_fraud THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 4
    ) AS tasa_fraude_pct
FROM fact_transactions f
JOIN dim_type t ON f.type_id = t.type_id
GROUP BY t.type
HAVING SUM(CASE WHEN f.is_fraud THEN 1 ELSE 0 END) > 0
ORDER BY tasa_fraude_pct DESC;
