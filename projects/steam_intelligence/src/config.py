from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SRC = ROOT / "src"

DATA = ROOT / "data"

RAW_DATA = DATA / "raw"

INTERIM_DATA = DATA / "interim"

PROCESSED_DATA = DATA / "processed"

MODELS = ROOT / "models"

REPORTS = ROOT / "reports"

NOTEBOOKS = ROOT / "notebooks"

CONFIG = ROOT / "config"

LOGS = ROOT / "logs"

TESTS = ROOT / "tests"