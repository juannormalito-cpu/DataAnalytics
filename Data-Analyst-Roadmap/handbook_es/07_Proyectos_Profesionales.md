# 07 · Proyectos Profesionales

*Parte 7 · Anterior: [06. Power BI](06_Power_BI.md)*

> 💡 **Qué vas a poder hacer después de este capítulo**
> Definir el alcance, estructurar y entregar un proyecto de la forma en que realmente pasa dentro de una empresa — no un notebook de Kaggle, sino un problema de negocio llevado desde la pregunta hasta el resumen ejecutivo.

---

## 7.1 La metodología

Cada proyecto en [`../proyectos/`](../proyectos/) sigue el mismo arco de siete pasos — que no es casualidad, es también cómo se define el alcance del trabajo real de un analista en una empresa:

```mermaid
flowchart LR
    A[1. Problema de Negocio] --> B[2. Datos y Esquema]
    B --> C[3. Preguntas a Responder]
    C --> D[4. SQL]
    D --> E[5. Python]
    E --> F[6. Power BI]
    F --> G[7. Resumen Ejecutivo]
```

1. **Problema de Negocio** — un párrafo, escrito como lo preguntaría realmente un stakeholder ("¿Por qué está subiendo el churn en el Noreste?"), no como una descripción de dataset.
2. **Diagrama de Base de Datos** — el esquema con el que estás trabajando, dibujado como en el [Capítulo 03](03_Bases_de_Datos.md).
3. **Preguntas a Responder** — 4–6 preguntas concretas en las que se descompone el problema de negocio.
4. **SQL** — extracción y agregación según el [Capítulo 04](04_SQL.md).
5. **Python** — limpieza, EDA e ingeniería de features según el [Capítulo 05](05_Python.md).
6. **Power BI** — el dashboard que los stakeholders realmente van a abrir, según el [Capítulo 06](06_Power_BI.md).
7. **Resumen Ejecutivo** — una página: qué encontraste, qué recomendás, qué necesitarías para ir más allá.

> ✅ **Buena práctica**
> Escribí el Resumen Ejecutivo **primero**, como hipótesis, antes de tocar el dato. Te obliga a plantear cómo sería una buena respuesta — y después el análisis o la confirma, o la mata, o la complica. Eso da una narrativa de proyecto mucho más sólida que "exploré el dato y encontré algunas cosas".

> ⚠️ **Error común**
> Liderar un proyecto con las herramientas ("Usé Python y Power BI para analizar datos de retail") en vez del problema de negocio. Los reclutadores y hiring managers hojean docenas de estos — los que se leen como un caso de negocio, no como una vidriera de herramientas, se destacan.

## 7.2 Estructura de carpetas del proyecto

Cada proyecto en [`../proyectos/`](../proyectos/) usa esta estructura:

```
proyectos/<NN_Nombre_Proyecto>/
├── README.md        # problema de negocio, objetivos, arquitectura, workflow, conclusiones
├── data/
├── sql/
├── python/
├── powerbi/
├── diagramas/
└── presentacion/
```

## 7.3 Los 10 proyectos

| # | Proyecto | Dificultad | Habilidades principales |
|---|---|---|---|
| 01 | Analítica de Ventas Retail | Principiante | SQL, Power BI |
| 02 | Churn de Clientes E-commerce | Intermedio | SQL, Python |
| 03 | BI de Adventure Works | Intermedio | SQL, Power BI |
| 04 | Operaciones Northwind | Principiante | SQL |
| 05 | Detección de Fraude con Tarjeta de Crédito | Avanzado | Python, ML |
| 06 | Analítica de Rotación de Personal (HR) | Intermedio | SQL, Python, Power BI |
| 07 | Performance de Campañas de Marketing | Intermedio | SQL, Power BI |
| 08 | Forecasting Financiero | Avanzado | Python, Series de Tiempo |
| 09 | Motor de Recomendación de Productos | Avanzado | Python, ML |
| 10 | Capstone: Pipeline End-to-End | Avanzado | SQL, Python, Power BI, ML |

---

## Resumen del capítulo

- Un proyecto real empieza con un problema de negocio planteado como lo preguntaría un stakeholder, no como una descripción de dataset.
- Estructura: Problema de Negocio → Esquema → Preguntas → SQL → Python → Power BI → Resumen Ejecutivo.
- Escribí el Resumen Ejecutivo como hipótesis primero — afila todo el análisis.
- Los 10 proyectos en [`../proyectos/`](../proyectos/) aplican esta metodología de punta a punta, aumentando en dificultad.

**Siguiente:** [08. Machine Learning →](08_Machine_Learning.md) — para los proyectos (05, 08, 09, 10) que van más allá de SQL/BI hacia el modelado predictivo.
