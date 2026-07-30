# shared-core

Librería interna compartida por los proyectos de `DataAnalytics/projects/`. Evita que cada
proyecto duplique config, logger, engine de base de datos y utilidades de IO.

## Contenido

- `shared_core.config` — carga de settings desde `.env` / variables de entorno.
- `shared_core.logging` — logger único (consola + archivo).
- `shared_core.database` — factory de engine de SQLAlchemy.
- `shared_core.io` — utilidades de lectura/escritura CSV.
- `shared_core.etl` — contratos base (`Extractor`, `Transformer`, `Loader`) para pipelines ETL.

## Regla de dependencias

`shared_core` no importa nada de `projects/`. Los proyectos dependen de `shared_core`,
nunca al revés.

## Instalación

Desde la carpeta de un proyecto:

```
pip install -e ../../shared
```

Instalar `shared-core` **antes** de instalar el proyecto.

> Nota: cada proyecto empaqueta su código como el paquete top-level `src` (ver su propio
> `pyproject.toml`). Si vas a instalar más de un proyecto en el mismo entorno virtual, usá
> un venv por proyecto — dos proyectos instalados a la vez en el mismo entorno colisionarían
> en el nombre de paquete `src`.
