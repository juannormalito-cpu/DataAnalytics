# DataAnalytics

Workspace (monorepo) para proyectos de Data Engineering / Analytics / ML. Cada proyecto en
`projects/` es independiente; comparten una librería interna (`shared/`) para no duplicar
config, logging, acceso a base de datos ni utilidades de IO.

## Estructura

```
DataAnalytics/
├── shared/          # librería interna instalable (shared_core): config, logging, database, io, etl
├── templates/        # scaffolding para crear proyectos nuevos (fuente única de verdad)
├── projects/          # cada carpeta es un proyecto independiente (Clean Architecture por dentro)
├── datasets/          # cache local de datasets crudos reutilizables entre proyectos (api/kaggle/postgres/public)
├── backups/           # dumps/backups de bases de datos (no se versiona el contenido)
├── dashboards/        # dashboards Streamlit que cruzan datos de más de un proyecto
├── docs/               # documentación del workspace (arquitectura, decisiones, runbooks)
├── portfolio/          # publicación/presentación de resultados de proyectos
└── scripts/            # automatización de workspace (ej. generador de proyectos)
```

Un dashboard o notebook que solo usa datos de **un** proyecto vive dentro de ese proyecto
(`projects/<nombre>/src/interfaces/`), no en `dashboards/` — esa carpeta es solo para vistas
que combinan varios proyectos.

## Regla de dependencias

```
interfaces → application → domain
     └────────→ infrastructure → shared_core
```

- `domain` no depende de nada externo ni de `shared_core`.
- `shared_core` nunca depende de nada dentro de `projects/`.
- Ningún proyecto importa código de otro proyecto directamente; lo que se comparte sube a `shared/`.

## Crear un proyecto nuevo

```bash
python scripts/create_project.py
```

Copia el template elegido a `projects/<nombre>/` y reemplaza los placeholders (`{{PROJECT_NAME}}`, etc).

`templates/base/` es el único template completo hoy. `templates/{api,dashboard,kaggle,machine_learning,streamlit}/`
son variantes reservadas (vacías, con `.gitkeep`) para cuando haga falta un scaffolding especializado
por tipo de entrega — deberían construirse como una copia de `base/` con el `interfaces/` correspondiente
ya resuelto (ej. `streamlit/` con `src/interfaces/dashboard.py`, `api/` con `src/interfaces/api/`).

## Instalar un proyecto para desarrollo local

```bash
pip install -e shared/
pip install -e projects/<nombre>
```

Instalar siempre `shared/` primero. Se recomienda un entorno virtual por proyecto: cada
proyecto empaqueta su código como el paquete top-level `src`, así que instalar dos proyectos
a la vez en el mismo entorno colisiona.

## Correr un proyecto

```bash
cd projects/<nombre>
python main.py
```

## Docker

Cada proyecto tiene su propio `Dockerfile`/`docker-compose.yml`, pero el build usa como
contexto la raíz del workspace (porque necesita copiar `shared/` además del proyecto):

```bash
docker compose -f projects/<nombre>/docker-compose.yml build
```
