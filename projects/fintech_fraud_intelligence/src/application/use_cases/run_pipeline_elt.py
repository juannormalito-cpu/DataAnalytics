"""
ELT pipeline: CSV -> clean/sample (Python) -> raw_transactions (Postgres) -> dbt run.

This replaces run_pipeline.py's ETL approach for the Star Schema tables —
Python now only extracts and loads raw data; dbt owns the transformation.
See README.md "SQL en producción: de ETL a ELT con dbt" for why.
"""

import os
import subprocess
from urllib.parse import parse_qs, urlparse

from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine
from sqlalchemy import text

from src.application.use_cases.extract_and_sample import extract_and_sample
from src.config import RAW_DATA, ROOT
from src.infrastructure.extractors.csv_extractor import PaySimCsvExtractor
from src.infrastructure.repositories.raw_repository import RawTransactionsLoader

DBT_DIR = ROOT / "dbt"


def database_url_to_dbt_env(database_url: str) -> dict:
    """dbt-postgres wants discrete host/user/password/dbname, not a single
    connection string — parse it once here instead of hand-maintaining two
    copies of the same credentials."""
    parsed = urlparse(database_url)
    query = parse_qs(parsed.query)
    return {
        "DBT_HOST": parsed.hostname or "",
        "DBT_USER": parsed.username or "",
        "DBT_PASSWORD": parsed.password or "",
        "DBT_PORT": str(parsed.port or 5432),
        "DBT_DBNAME": parsed.path.lstrip("/"),
        "DBT_SSLMODE": query.get("sslmode", ["require"])[0],
    }


def run_pipeline_elt() -> None:
    print("Pipeline ELT inicializado.")

    # -------------------------------
    # Extract
    # -------------------------------
    extractor = PaySimCsvExtractor(RAW_DATA / "paysim.csv")
    raw = extractor.extract()
    print(f"  extraídas {len(raw):,} transacciones crudas")

    # -------------------------------
    # Sample (la única lógica de negocio que se queda en Python)
    # -------------------------------
    sampled = extract_and_sample(raw)

    # -------------------------------
    # Load crudo (sin transformar) a Postgres
    # -------------------------------
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)
    loader = RawTransactionsLoader(engine)
    loader.load(sampled)

    # -------------------------------
    # Liberar espacio antes de que dbt reconstruya el Star Schema — el plan
    # gratuito de Neon tiene un límite de 512MB, y raw_transactions + las
    # tablas viejas coexistiendo lo supera. dbt va a recrear estas tablas
    # de todos modos, así que no hay pérdida de datos real acá.
    # -------------------------------
    print("\nLiberando espacio (tablas que dbt va a reconstruir)...")
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS fraud_scores CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS fact_transactions CASCADE"))

    # -------------------------------
    # Transform: dbt toma el control desde acá
    # -------------------------------
    print("\nCorriendo dbt run...")
    dbt_env = {**os.environ, **database_url_to_dbt_env(settings.database_url)}
    result = subprocess.run(
        ["dbt", "run", "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)],
        env=dbt_env, cwd=DBT_DIR,
    )
    if result.returncode != 0:
        raise SystemExit("dbt run falló — ver output arriba.")

    print("\nCorriendo dbt test...")
    subprocess.run(
        ["dbt", "test", "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)],
        env=dbt_env, cwd=DBT_DIR,
    )

    print("\nPipeline ELT finalizado. Star Schema recreado por dbt (dim_time, dim_type, fact_transactions).")


if __name__ == "__main__":
    run_pipeline_elt()
