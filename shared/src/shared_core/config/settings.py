import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    database_url: str
    log_level: str


def load_settings(env_file: Path | None = None) -> Settings:
    load_dotenv(dotenv_path=env_file)

    return Settings(
        database_url=os.environ.get("DATABASE_URL", ""),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )
