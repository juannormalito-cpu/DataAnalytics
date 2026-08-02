# 09 · Portfolio y Carrera

*Parte 9 · Anterior: [08. Machine Learning](08_Machine_Learning.md)*

> 💡 **Qué vas a poder hacer después de este capítulo**
> Empaquetar todo lo de los Capítulos 1–8 en un portfolio y una búsqueda laboral que realmente convierta — higiene de Git, un CV que se lee como impacto en vez de tareas, preparación de entrevistas, y un camino hacia el freelancing si querés uno.

---

## 9.1 Git y GitHub

```bash
git init
git add .
git commit -m "Agregar análisis de churn de clientes: extracción SQL + EDA en Python"
git remote add origin <tu-url-de-repo>
git push -u origin main
```

> ✅ **Buena práctica**
> Comiteá en bloques significativos con mensajes que describan *por qué*, no "update file" — un hiring manager que hojea tu historial de commits está evaluando silenciosamente cómo vas a trabajar en su equipo. Esta es la misma disciplina que modela el propio [`CHANGELOG.md`](../CHANGELOG.md) de este handbook.

## 9.2 README y Estructura de Proyecto

Cada proyecto ([Capítulo 07](07_Proyectos_Profesionales.md)) necesita un README que un reclutador pueda leer en 60 segundos y entender: **Cuál era el problema de negocio, qué hiciste, qué encontraste.** Empezá con una captura del dashboard o un gráfico clave — no con una pared de texto.

> ⚠️ **Error común**
> Un perfil de GitHub con 15 repos de tutoriales seguidos al pie de la letra ("Notebook Titanic #1") y cero proyectos terminados y narrados. Tres proyectos completos con un planteo real de negocio (según el [Capítulo 07](07_Proyectos_Profesionales.md)) le ganan a quince sin terminar, siempre.

## 9.3 LinkedIn y CV

**Fórmula para bullets del CV:** `[Acción] + [qué analizaste/construiste] + [impacto de negocio cuantificado]`

| Débil | Fuerte |
|---|---|
| "Usé SQL y Python para analizar datos de ventas" | "Identifiqué una fuga de revenue de $180k/año en un bug de acumulación de descuentos usando análisis de cohortes en SQL; recomendación adoptada por Finanzas" |
| "Construí dashboards en Power BI" | "Construí un dashboard ejecutivo en Power BI adoptado por 3 equipos regionales, reemplazando 6 horas/semana de reportes manuales" |

> ✅ **Buena práctica**
> Cada bullet debería sobrevivir a la pregunta "¿y qué?". Si no termina en un resultado que le importe a alguien de negocio, reescribilo.

## 9.4 Preguntas de Entrevista

**Ronda de SQL** (ver también [Capítulo 04](04_SQL.md)):
- Escribí una query para encontrar el segundo salario más alto por departamento.
- Explicá la diferencia entre `WHERE` y `HAVING`.
- Dadas dos tablas, escribí una query para encontrar clientes sin pedidos.

**Ronda de Python** (ver también [Capítulo 05](05_Python.md)):
- Dado un DataFrame desordenado, explicá en voz alta tu enfoque de limpieza.
- Explicá `.groupby()` vs. una tabla dinámica — ¿cuándo usarías cada uno?

**Ronda de caso de negocio:**
- "Los usuarios activos semanales bajaron 10% la semana pasada — contame cómo lo investigarías."
- Practicá estructurar tu respuesta: aclarar la definición de la métrica → chequear problemas de datos → segmentar (por plataforma, geografía, cohorte) → formular y testear una hipótesis → recomendar próximos pasos.

**Ronda de ML** (ver también [Capítulo 08](08_Machine_Learning.md)):
- Precision vs. Recall — ¿cuándo optimizás por uno sobre el otro?
- ¿Cómo sabés si un modelo está haciendo overfitting?

## 9.5 Freelancing (Fiverr, Upwork)

El trabajo freelance en datos es una forma legítima de construir portfolio *e* ingresos mientras buscás trabajo:

- Empezá con proyectos chicos y bien acotados: "limpiame y analizame este dataset," "construime un dashboard de 3 páginas en Power BI."
- Cobrá por el entregable, no por hora, una vez que tengas 2-3 reseñas.
- Cada proyecto freelance es un proyecto de portfolio — aplicale la estructura del [Capítulo 07](07_Proyectos_Profesionales.md) también.

> ⚠️ **Error común**
> Cobrar de menos para ganar el primer trabajo, y quedarte cobrando de menos para siempre. Bajá el precio solo para tus primeras 2-3 reseñas, y después subí tus tarifas — las reseñas son el activo que realmente estás comprando en esa etapa.

## 9.6 Cronogramas de Aprendizaje

| Track | Ritmo | Distribución aproximada por capítulo |
|---|---|---|
| **6 meses** (intensivo, ~25-30 hs/sem) | Cap.01–03: 2 sem · SQL: 4 sem · Python: 5 sem · Power BI: 3 sem · Proyectos: 6 sem · ML: 4 sem · Portfolio/búsqueda laboral: continuo desde el mes 4 |
| **12 meses** (balanceado, ~12-15 hs/sem) | Mismo orden, aproximadamente el doble de tiempo por fase, con 2 proyectos corriendo en paralelo con cada nueva habilidad |
| **18 meses** (part-time, ~6-8 hs/sem) | Mismo orden, un tema a la vez, mínimo 1 proyecto entregado por trimestre |

## 9.7 Consejos de un Ingeniero Senior

> 🏢 **Desde las trincheras**
> - "Los mejores analistas que contraté no eran los mejores en SQL — eran los mejores en preguntar '¿es esta la pregunta correcta?' antes de escribir cualquier query."
> - "En tus primeros seis meses en el trabajo, sobre-comunicá los supuestos. Un número incorrecto que nadie cuestionó es peor que un número lento en el que todos confían."
> - "No esperes permiso para tener curiosidad sobre una métrica que se ve rara. Ese instinto es el trabajo en sí."

---

## Resumen del capítulo

- La higiene de Git/GitHub y un README que lidera con impacto de negocio son parte del entregable, no un detalle secundario.
- Los bullets del CV deberían sobrevivir a "¿y qué?" — cuantificá el impacto de negocio, no solo las herramientas usadas.
- Preparate para cuatro frentes de entrevista: SQL, Python, caso de negocio, y (si aplica) ML.
- El freelancing es un camino paralelo legítimo — tratá cada trabajo como un proyecto de portfolio.
- Elegí un cronograma (6/12/18 meses) que coincida con tus horas reales disponibles, no con tu ambición.

**Esto completa el handbook central.** Volvé a la Tabla de Contenidos · Continuá con los [10 proyectos de portfolio](../proyectos/) para aplicar todo.
