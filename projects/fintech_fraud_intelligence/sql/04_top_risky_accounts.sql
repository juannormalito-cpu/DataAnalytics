-- Cuentas de origen con más transacciones marcadas como fraude, o con
-- inconsistencias de balance (balance_mismatch) — lista accionable para el
-- equipo de Riesgo, el mismo patrón LEFT JOIN/CTE de handbook_es/04_SQL.md.
WITH riesgo_por_cuenta AS (
    SELECT
        origin_account_id,
        COUNT(*)                                             AS total_transacciones,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END)             AS fraudes,
        SUM(CASE WHEN balance_mismatch THEN 1 ELSE 0 END)     AS inconsistencias_balance,
        SUM(amount)                                           AS monto_total_movido
    FROM fact_transactions
    GROUP BY origin_account_id
)
SELECT *
FROM riesgo_por_cuenta
WHERE fraudes > 0 OR inconsistencias_balance > 0
ORDER BY fraudes DESC, inconsistencias_balance DESC
LIMIT 100;
