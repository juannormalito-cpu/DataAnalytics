# 04 · SQL — El Curso Completo

*Parte 4 · Anterior: [03. Bases de Datos](03_Bases_de_Datos.md)*

> 💡 **Qué vas a poder hacer después de este capítulo**
> Escribir SQL analítico real de punta a punta — filtrando, agregando, uniendo, usando funciones de ventana y optimizando — contra el Star Schema del [Capítulo 03](03_Bases_de_Datos.md). Esta es la habilidad de mayor impacto en todo el handbook.

Todos los ejemplos usan el esquema `fact_ventas` / `dim_producto` / `dim_cliente` / `dim_fecha` / `dim_tienda` introducido en [03.3](03_Bases_de_Datos.md#33-star-schema-vs-snowflake-schema).

---

## 4.1 SELECT, WHERE, ORDER BY

```sql
SELECT nombre_producto, categoria, precio
FROM dim_producto
WHERE categoria = 'Electrónica'
ORDER BY precio DESC;
```

> 🏢 **Caso de negocio:** Marketing pide "todos los productos de Electrónica con precio mayor a $50, del más caro al más barato" para planear una promo.

**Ejercicio:** Listá todos los clientes que se registraron en 2025, ordenados por fecha de registro.
<details><summary>Solución</summary>

```sql
SELECT cliente_id, nombre, fecha_registro
FROM dim_cliente
WHERE fecha_registro >= '2025-01-01' AND fecha_registro < '2026-01-01'
ORDER BY fecha_registro;
```
</details>

---

## 4.2 GROUP BY, HAVING

`GROUP BY` colapsa filas en grupos; `HAVING` filtra *después* de la agregación (`WHERE` filtra *antes*).

```sql
SELECT categoria, SUM(revenue) AS revenue_total
FROM fact_ventas f JOIN dim_producto p ON f.producto_id = p.producto_id
GROUP BY categoria
HAVING SUM(revenue) > 100000;
```

> 🏢 **Caso de negocio:** Finanzas quiere solo las categorías que generaron más de $100k — las categorías chicas son ruido para esta revisión.

**Ejercicio:** Encontrá las tiendas con más de 500 pedidos en total.
<details><summary>Solución</summary>

```sql
SELECT tienda_id, COUNT(*) AS cantidad_pedidos
FROM fact_ventas
GROUP BY tienda_id
HAVING COUNT(*) > 500;
```
</details>

---

## 4.3 JOIN, UNION

| Tipo de JOIN | Devuelve |
|---|---|
| `INNER JOIN` | Solo filas que coinciden en ambas tablas |
| `LEFT JOIN` | Todas las filas de la tabla izquierda, filas coincidentes de la derecha (NULL si no hay match) |
| `RIGHT JOIN` | Espejo de LEFT JOIN |
| `FULL OUTER JOIN` | Todas las filas de ambas, coincidentes donde sea posible |

```sql
-- Clientes que todavía no hicieron ningún pedido (uso clásico de LEFT JOIN)
SELECT c.cliente_id, c.nombre
FROM dim_cliente c
LEFT JOIN fact_ventas f ON c.cliente_id = f.cliente_id
WHERE f.cliente_id IS NULL;
```

`UNION` apila resultados verticalmente (y elimina duplicados; `UNION ALL` los mantiene — y es más rápido).

> 🏢 **Caso de negocio:** Growth quiere una lista de "nunca compró" para una campaña de descuento de primera compra — exactamente el patrón `LEFT JOIN ... WHERE ... IS NULL` de arriba.

**Ejercicio:** Combiná una lista de pedidos online y pedidos en tienda física en un solo resultado, manteniendo duplicados.
<details><summary>Solución</summary>

```sql
SELECT pedido_id, 'online' AS canal FROM pedidos_online
UNION ALL
SELECT pedido_id, 'tienda' AS canal FROM pedidos_tienda;
```
</details>

---

## 4.4 CTEs y Subconsultas

Un **CTE** (Common Table Expression, `WITH`) nombra una subconsulta para que puedas construir una query en pasos legibles.

```sql
WITH revenue_mensual AS (
    SELECT DATE_TRUNC('month', d.fecha_completa) AS mes, SUM(f.revenue) AS revenue
    FROM fact_ventas f JOIN dim_fecha d ON f.fecha_id = d.fecha_id
    GROUP BY 1
)
SELECT mes, revenue,
       revenue - LAG(revenue) OVER (ORDER BY mes) AS cambio_mensual
FROM revenue_mensual
ORDER BY mes;
```

> ✅ **Buena práctica**
> Preferí CTEs por sobre subconsultas anidadas en profundidad — se leen de arriba hacia abajo como una narrativa, y cualquier analista de tu equipo puede debuggearlas pieza por pieza.

**Ejercicio:** Encontrá el cliente que más gastó por región usando un CTE.
<details><summary>Solución</summary>

```sql
WITH totales_cliente AS (
    SELECT c.region, c.cliente_id, SUM(f.revenue) AS total_gastado
    FROM fact_ventas f JOIN dim_cliente c ON f.cliente_id = c.cliente_id
    GROUP BY c.region, c.cliente_id
),
ranking AS (
    SELECT *, RANK() OVER (PARTITION BY region ORDER BY total_gastado DESC) AS rnk
    FROM totales_cliente
)
SELECT region, cliente_id, total_gastado
FROM ranking
WHERE rnk = 1;
```
</details>

---

## 4.5 Vistas y Procedimientos Almacenados

- **Vista (View):** una query guardada de la que podés hacer `SELECT` como si fuera una tabla — genial para ocultar complejidad de otros analistas.
- **Procedimiento almacenado (Stored Procedure):** un bloque de SQL (y lógica) guardado y parametrizado al que llamás con `CALL` — lo usan más los engineers que los analistas, pero deberías reconocer uno cuando lo veas.

```sql
CREATE VIEW vw_revenue_mensual_categoria AS
SELECT DATE_TRUNC('month', d.fecha_completa) AS mes, p.categoria, SUM(f.revenue) AS revenue
FROM fact_ventas f
JOIN dim_fecha d ON f.fecha_id = d.fecha_id
JOIN dim_producto p ON f.producto_id = p.producto_id
GROUP BY 1, 2;
```

> 🏢 **Caso de negocio:** En vez de que cada analista reescriba el mismo join de 3 tablas cada semana para el dashboard ejecutivo, un **Analytics Engineer** lo expone como una vista — esta es exactamente la idea de "única fuente de verdad" del [01.2](01_Introduccion.md).

---

## 4.6 Funciones de Ventana y Ranking

Las funciones de ventana calculan sobre un conjunto de filas *relacionadas con la fila actual*, sin colapsarlas como hace `GROUP BY`.

| Función | Uso |
|---|---|
| `ROW_NUMBER()` | Número secuencial único por fila |
| `RANK()` / `DENSE_RANK()` | Ranking con (`RANK`) o sin (`DENSE_RANK`) huecos en empates |
| `LAG()` / `LEAD()` | Valor de una fila anterior/siguiente |
| `SUM()/AVG() OVER (...)` | Totales acumulados, promedios móviles |

```sql
SELECT
    cliente_id, fecha_pedido, revenue,
    SUM(revenue) OVER (PARTITION BY cliente_id ORDER BY fecha_pedido) AS total_acumulado
FROM fact_ventas;
```

> 🏢 **Caso de negocio:** "Mostrame el gasto acumulado de por vida de cada cliente a lo largo del tiempo" — la pregunta clásica de función de ventana de total acumulado, y una de las preguntas de entrevista de SQL más comunes.

**Ejercicio:** Para cada producto, rankeá sus ventas por revenue dentro de su categoría.
<details><summary>Solución</summary>

```sql
SELECT
    p.categoria, p.nombre_producto, f.revenue,
    DENSE_RANK() OVER (PARTITION BY p.categoria ORDER BY f.revenue DESC) AS rank_en_categoria
FROM fact_ventas f JOIN dim_producto p ON f.producto_id = p.producto_id;
```
</details>

---

## 4.7 Performance, Índices y Optimización

> ⚠️ **Errores comunes**
> - `SELECT *` en una tabla ancha del warehouse cuando necesitás 3 columnas — lee muchos más datos de los necesarios.
> - Filtrar sobre una función aplicada a una columna (`WHERE YEAR(fecha_pedido) = 2026`) — esto a menudo impide que la base de datos use un índice. Preferí `WHERE fecha_pedido >= '2026-01-01' AND fecha_pedido < '2027-01-01'`.
> - Hacer join sobre columnas sin índice en tablas grandes — consultá con tu Data Engineer si un camino de join muy usado está lento.

> ✅ **Buenas prácticas**
> - Filtrá lo antes posible (`WHERE` antes de unir más tablas de las necesarias).
> - Leé el **plan de ejecución** (`EXPLAIN` / `EXPLAIN ANALYZE`) cuando una query esté inesperadamente lenta — te dice si está escaneando una tabla completa o usando un índice.
> - Agregá al nivel más grueso que realmente necesite la pregunta — no traigas datos fila por fila a Python solo para sumarlos ahí.

---

## Resumen del capítulo

- `SELECT/WHERE/ORDER BY` → `GROUP BY/HAVING` → `JOIN` son el 80% diario del SQL de un analista.
- Los CTEs hacen legible la lógica de varios pasos; las Vistas exponen esa lógica como bloques reutilizables y confiables.
- Las funciones de ventana resuelven problemas de "comparar esta fila con otras filas" sin colapsar tu conjunto de resultados — rankings, totales acumulados, cambio período a período.
- La performance de queries se trata mayormente de filtrar temprano, evitar funciones sobre columnas filtradas, y leer el plan de ejecución cuando algo está lento.

**Siguiente:** [05. Python →](05_Python.md) — donde el output de SQL se convierte en limpieza, EDA e ingeniería de features.
