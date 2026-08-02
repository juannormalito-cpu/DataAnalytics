-- Tendencia diaria: volumen, monto, y monto en fraude — con % de cambio día a día
-- usando LAG(), igual que handbook_es/04_SQL.md §4.6 (funciones de ventana).
WITH diario AS (
    SELECT
        dt.day,
        COUNT(*)                                                    AS transacciones,
        SUM(f.amount)                                               AS monto_total,
        SUM(CASE WHEN f.is_fraud THEN f.amount ELSE 0 END)          AS monto_fraude
    FROM fact_transactions f
    JOIN dim_time dt ON f.time_id = dt.time_id
    GROUP BY dt.day
)
SELECT
    day,
    transacciones,
    monto_total,
    monto_fraude,
    ROUND(
        (
            100.0 * (monto_total - LAG(monto_total) OVER (ORDER BY day))
            / NULLIF(LAG(monto_total) OVER (ORDER BY day), 0)
        )::numeric, 2
    ) AS cambio_dia_anterior_pct
FROM diario
ORDER BY day;
