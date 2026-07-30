import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import find_dotenv, load_dotenv


@dataclass(frozen=True)
class Settings:
    database_url: str
    log_level: str


def load_settings(env_file: Path | None = None) -> Settings:
    # Pasar env_file explícito (ej. ROOT / ".env" desde src/config.py) es lo confiable:
    # ni el cwd ni la ubicación de este módulo (instalado en shared/, fuera del proyecto)
    # tienen por qué coincidir con la carpeta del proyecto — un dashboard de Streamlit,
    # por ejemplo, corre con el cwd del workspace, no el del proyecto. find_dotenv(usecwd)
    # queda solo como fallback para scripts sueltos que no pasan env_file.
    load_dotenv(dotenv_path=env_file or find_dotenv(usecwd=True))

    return Settings(
        database_url=os.environ.get("DATABASE_URL", ""),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
