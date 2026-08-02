# Mapa del workspace

Documento de referencia para orientarse rápido en este monorepo — pensado para compartir con otro agente/colaborador que vaya a seguir expandiendo el portfolio.

---

## Estructura

```
DataAnalytics/                          (monorepo — GitHub: juannormalito-cpu/DataAnalytics)
├── shared/shared_core/                 librería interna instalable: config, logging, database, io, etl
├── templates/                          scaffolding para proyectos nuevos: api, base, dashboard, kaggle, machine_learning, streamlit
├── scripts/create_project.py           genera un proyecto nuevo copiando un template
├── projects/
│   ├── agro_intelligence/              ganadería/agricultura/forestación — deployado en Streamlit Community Cloud
│   ├── steam_intelligence/             scaffold creado, sin implementar
│   ├── ci_smoke_test/                  proyecto mínimo para validar que el CI funciona
│   └── fintech_fraud_intelligence/     el más completo — pipeline ELT, ML, API, portfolio
├── Data-Analyst-Roadmap/               handbook propio (español + inglés), 9 capítulos, PDF, Notion
├── datasets/{api,kaggle,postgres,public}/   cache de datasets crudos compartido entre proyectos (contenido gitignored)
├── dashboards/                         para vistas que cruzan datos de más de un proyecto (vacío hoy)
├── docs/, backups/, portfolio/         scaffolds vacíos (`.gitkeep`), sin contenido todavía
└── .github/workflows/ci.yml            CI real: ruff + pytest por proyecto, en cada push/PR a GitHub Actions
```

**Regla de dependencias** (Clean Architecture, aplicada dentro de cada proyecto):
```
interfaces → application → domain
     └────────→ infrastructure → shared_core
```
`domain` no depende de nada externo. `shared_core` nunca depende de nada dentro de `projects/`. Ningún proyecto importa código de otro directamente — lo compartido sube a `shared/`.

---

## `fintech_fraud_intelligence` — el proyecto de referencia

El más desarrollado del workspace — vale la pena usarlo como plantilla de calidad para los demás.

```
fintech_fraud_intelligence/
├── src/
│   ├── domain/              entidad Transaction, sin I/O
│   ├── application/          casos de uso: pipelines (ETL viejo + ELT nuevo), transformaciones, entrenamiento de modelo
│   ├── infrastructure/        extractors (CSV), repositories (Postgres: Star Schema completo y solo-crudo)
│   └── interfaces/           CLI, API (FastAPI), EDA, entrenamiento, SHAP, calibración, streaming simulado, orquestación (Prefect)
├── dbt/                      transformación SQL versionada y testeada (17 tests)
├── sql/                      5 queries de análisis de negocio
├── powerbi/                  modelo y medidas DAX para el dashboard
├── presentation/             landing page de portfolio (HTML/CSS/JS autónomo, publicado como Claude Artifact)
├── data/, models/, reports/  artefactos generados (gitignored el contenido pesado)
└── render.yaml, Procfile      config de deploy lista (Render/Railway)
```

---

## Conectividades externas activas

| Conexión | Estado | Detalle |
|---|---|---|
| **GitHub** | Conectado | `origin` → tu repo real. CI en Actions corre lint + tests en cada push/PR |
| **Neon (Postgres)** | Conectado y en uso | `fintech_fraud_intelligence` corre 100% contra la base real en la nube |
| **Kaggle** | Fuente de datos | Descarga manual (requiere cuenta, no se automatiza) |
| **dbt** | Conectado a Neon | Transforma dentro de la misma base vía `DATABASE_URL` parseada a variables de entorno |
| **Prefect** | Local únicamente | Corre como proceso Python; para que sea autónomo de verdad falta un Prefect Cloud o server propio 24/7 |
| **Power BI** | Conectado a Neon | El `.pbix` se conecta directo a la misma base |
| **Claude Artifacts** | Publicado | Landing page en URL propia, republicable desde una conversación con el archivo fuente |
| **Render / Railway** | Preparado, no desplegado | `render.yaml`/`Procfile` listos — falta crear la cuenta y conectar el repo |
| **Streamlit Community Cloud** | Desplegado | Para `agro_intelligence`, no para `fintech_fraud_intelligence` |
| **Notion** | Automatización lista, no ejecutada | Script + prompt en `Data-Analyst-Roadmap/notion/` para levantar el workspace de Notion |

---

## Estado de git al momento de escribir esto

Todo lo generado en la sesión que armó `fintech_fraud_intelligence` y `Data-Analyst-Roadmap` estaba **sin commitear** hasta este documento. Antes de seguir expandiendo, confirmá que ese commit ya se hizo (`git log` en la rama actual) — si no, es el primer paso.

## Pendientes conocidos (no bloqueantes)

- `dashboards/`, `docs/`, `backups/`, `portfolio/` siguen vacíos — están en el plan del workspace pero sin contenido real todavía.
- `steam_intelligence` es un scaffold sin implementar.
- El drill-through de Power BI en `fintech_fraud_intelligence` quedó descartado por fricción de UI (documentado en su propio README).
- Deploy real de la API de fintech (Render/Railway) y del workspace de Notion: configurados pero no ejecutados.
