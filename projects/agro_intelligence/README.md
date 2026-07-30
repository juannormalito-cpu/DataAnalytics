# agro_intelligence

## Description

Inteligencia de datos agropecuaria para empresas de la zona núcleo + litoral (Buenos Aires,
Santa Fe, Entre Ríos, Corrientes, Córdoba), dividida en **ganadería**, **agricultura** y
**forestación**, con un motor financiero (VAN/TIR/payback) para evaluar proyectos productivos
desde la vista de la empresa que busca financiamiento.

---

## Fuentes de datos (verificadas, ver `src/application/use_cases/ingest_series.py`)

| Vertical | Fuente | Variable |
|---|---|---|
| Agricultura | MAGyP — Estimaciones Agrícolas | Rendimiento (kg/ha) de soja/maíz/trigo por provincia/año |
| Agricultura / Insumos | CommodityPriceAPI (CBOT) | Precio internacional soja/maíz/trigo y urea, USD/ton — **proxy**: Argentina no publica FAS/FOB en serie abierta, solo PDF |
| Ganadería | MAGyP/datos.gob.ar — Mercado de Liniers | Precio de novillo ($/kg vivo), serie nacional mensual |
| Forestación | Ministerio de Ambiente — Bosque nativo | Superficie de bosque nativo (proxy — **no** es superficie implantada comercial; esa fuente sigue pendiente) |
| Macro | API de Series de Tiempo (BCRA/MAE/Rofex) | Tipo de cambio oficial mayorista (A3500) |
| Macro | api.argentinadatos.com | Dólar blue (venta), diario desde 2011 |

El CSV de Estimaciones Agrícolas mezcla encodings de casi 55 años de historia (1969-2024) y
tiene filas con caracteres corruptos en el origen — el filtro de cultivo/provincia en
`AgricultureTransformer` tolera eso a propósito, no asume un encoding "limpio" que la fuente
no tiene.

`COMMODITY_API_KEY` (plan "lite", 2000 requests) va en `.env`, nunca en el código. La
profundidad histórica varía por símbolo (soja desde ~2015, maíz recién desde 2023) — el
extractor tolera años sin datos en vez de asumir una fecha de arranque uniforme. El
metadata de la API dice que el trigo (`ZW-SPOT`) cotiza en USD, pero es falso — verificado
contra el pico real de mayo 2022, en realidad cotiza en centavos como soja/maíz.

## Zonificación departamental y valores de referencia

- `rendimiento_{cultivo}_depto` — el mismo CSV de estimaciones agrícolas, agrupado por
  departamento en vez de provincia (25.759 observaciones, ~190 departamentos). Los
  centroides para ubicarlos en el mapa vienen de `apis.datos.gob.ar/georef` (oficial). No
  todos matchean por nombre entre las dos fuentes — el dashboard muestra cuántos quedan
  afuera en vez de ocultarlo.
- **Arrendamiento y precio de tierra NO son series ingeridas** — no hay fuente argentina
  abierta y estructurada para ninguno de los dos (solo PDFs de MAGyP y notas de prensa). Se
  usan como valores de referencia puntuales, citados y fechados, en
  `src/application/use_cases/reference_values.py`:
  - Arrendamiento: Bolsa de Cereales de Córdoba, campaña 2025/26 (quintales/ha por zona).
  - Precio de tierra: rangos de Agrofy News/Perfil — solo hay para Buenos Aires, Santa Fe
    y Córdoba; para Entre Ríos/Corrientes no encontré una fuente citable.
- **Retenciones** (`src/domain/taxation.py`): tasas reales del Decreto 423/2026 (soja 24%,
  maíz/sorgo 8.5%, trigo/cebada 5.5%). Es la única carga impositiva agro uniforme a nivel
  nacional — Ganancias, Ingresos Brutos e Impuesto Inmobiliario Rural varían por provincia
  y situación fiscal, y **no** se estiman (se marcan como "consultar contador" en vez de
  inventar una tasa que probablemente esté mal).

---

## Estructura

- `src/domain/` — `timeseries.py` (Variable/Observation genéricos), `finance.py` (VAN/TIR/payback,
  vertical-agnóstico), `agriculture.py`/`livestock.py`/`forestry.py` (una regla real por vertical).
- `src/application/use_cases/` — `ingest_series.py` (Extractor→Transformer→Loader por fuente),
  `evaluate_project.py` (evaluación financiera de un flujo de fondos).
- `src/infrastructure/` — extractors (CSV de MAGyP/ambiente, API de series de tiempo) y el
  repositorio de series en Postgres.
- `src/interfaces/cli.py` — `python main.py ingest` / `python main.py evaluate`.
- `src/interfaces/dashboard.py` — dashboard Streamlit con 8 pestañas: series históricas (filtro
  de fecha + proyección de tendencia), estadísticas descriptivas + histograma, mapa geográfico
  (departamento o provincia, con leyenda y ranking top/bottom), series apiladas (índice base
  100), comparativa anual (ingreso bruto por cultivo), matriz de correlación + cruce de
  variables, asistente de zona (rinde/arrendamiento/precio de tierra/retenciones), y evaluador
  de proyecto.
- `data/`, `models/`, `reports/`, `notebooks/` — artefactos generados, gitignored salvo estructura.
- `tests/unit/`, `tests/integration/`

---

## Setup

```bash
pip install -e ../../shared
pip install -e .
cp .env.example .env
```

## Run

```bash
python main.py ingest     # trae y persiste las series históricas
python main.py evaluate   # corre una evaluación VAN/TIR de ejemplo
streamlit run src/interfaces/dashboard.py   # dashboard interactivo
```

---

## Compartir el dashboard (Streamlit Community Cloud + Neon)

Ya está ingerido en una base Neon (Postgres gratis en la nube), verificado con
`.streamlit/secrets.toml` local antes de subir nada:

1. Subir este repo a GitHub.
2. En [share.streamlit.io](https://share.streamlit.io): conectar el repo, archivo principal
   `projects/agro_intelligence/src/interfaces/dashboard.py`.
3. En **Settings → Secrets** de la app, pegar el contenido de
   `.streamlit/secrets.toml.example` con los valores reales (`DATABASE_URL` de Neon, etc.)
   — nunca en el código ni en el repo.

`dashboard.py` copia `st.secrets` a variables de entorno al arrancar (Streamlit Cloud no
las expone como env vars por sí solo) — probado localmente sacando el `.env` del medio y
confirmando que sigue andando solo con `.streamlit/secrets.toml` (gitignored).

Para reingestar contra una base distinta a la local sin tocar `.env`:

```bash
DATABASE_URL="postgresql://..." python main.py ingest
```

---

## Roadmap

1. ✅ Esqueleto + dominio + un extractor real por vertical + motor financiero.
2. ✅ Dashboard Streamlit sobre los datos ya ingeridos (series históricas + evaluador).
3. ✅ Filtro de fecha, dólar blue, precio de granos/insumos, comparativa anual por ingreso
   bruto real, cruce de variables, proyección de tendencia y narrativa automática.
4. ✅ Zonificación departamental en el mapa, series apiladas, asistente de zona (rinde,
   arrendamiento, precio de tierra, retenciones).
5. Noticias y cambios de precio en la cadena (con lectura de noticias, no solo tendencia).
6. Manual gráfico del modelo + UX de los dashboards.

---

## Technologies

- Python, Pandas, SQLAlchemy, PostgreSQL
- requests (APIs públicas), numpy-financial (VAN/TIR)

---

## Author

Facu
