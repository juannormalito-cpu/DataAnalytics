-- Volumen de transacciones y monto total, por tipo y por hora del día.
-- Responde: "¿cuándo y en qué canal se concentra el movimiento de dinero?"
SELECT
    t.type,
    dt.hour_of_day,
    COUNT(*)                       AS cantidad_transacciones,
    SUM(f.amount)                  AS monto_total,
    ROUND(AVG(f.amount)::numeric, 2) AS monto_promedio
FROM fact_transactions f
JOIN dim_type t ON f.type_id = t.type_id
JOIN dim_time dt ON f.time_id = dt.time_id
GROUP BY t.type, dt.hour_of_day
ORDER BY t.type, dt.hour_of_day;
