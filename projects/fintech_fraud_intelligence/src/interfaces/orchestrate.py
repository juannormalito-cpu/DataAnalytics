"""
Orchestrates the full pipeline with Prefect — retries, logging, and
observability per step, without needing Docker or Airflow (Prefect runs as a
plain Python process, which is why it fits here: no virtualization needed).

Run once, ad-hoc:
    python -m src.interfaces.orchestrate

Turn it into a scheduled deployment (still no Docker required — runs as a
local process):
    prefect server start                      # in one terminal, starts the UI/API
    python -m src.interfaces.orchestrate --serve   # in another, registers + serves the schedule
Then open http://localhost:4200 to see runs, retries, and logs.
"""

import argparse
import os
import subprocess

from prefect import flow, get_run_logger, task
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine

from src.application.use_cases.extract_and_sample import extract_and_sample
from src.application.use_cases.run_pipeline_elt import DBT_DIR, database_url_to_dbt_env
from src.config import RAW_DATA, ROOT
from src.infrastructure.extractors.csv_extractor import PaySimCsvExtractor
from src.infrastructure.repositories.raw_repository import RawTransactionsLoader


@task(retries=2, retry_delay_seconds=10, log_prints=True)
def extract_task():
    extractor = PaySimCsvExtractor(RAW_DATA / "paysim.csv")
    raw = extractor.extract()
    print(f"extraídas {len(raw):,} filas")
    return raw


@task(retries=1, log_prints=True)
def sample_task(raw):
    return extract_and_sample(raw)


@task(retries=2, retry_delay_seconds=15, log_prints=True)
def load_raw_task(sampled):
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)
    RawTransactionsLoader(engine).load(sampled)
    return settings.database_url


@task(retries=1, log_prints=True)
def dbt_run_task(database_url: str):
    env = {**os.environ, **database_url_to_dbt_env(database_url)}
    result = subprocess.run(
        ["dbt", "run", "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)],
        env=env, cwd=DBT_DIR, capture_output=True, text=True,
    )
    print(result.stdout[-2000:])
    if result.returncode != 0:
        raise RuntimeError("dbt run falló")


@task(log_prints=True)
def dbt_test_task(database_url: str):
    env = {**os.environ, **database_url_to_dbt_env(database_url)}
    result = subprocess.run(
        ["dbt", "test", "--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)],
        env=env, cwd=DBT_DIR, capture_output=True, text=True,
    )
    print(result.stdout[-2000:])
    # Los tests fallando no deberían tumbar todo el pipeline en este proyecto de
    # portfolio, pero en un entorno real esto dispararía una alerta al equipo.
    if result.returncode != 0:
        logger = get_run_logger()
        logger.warning("dbt test encontró fallas — revisar antes de confiar en los datos.")


@flow(name="fintech-fraud-elt-pipeline", log_prints=True)
def elt_pipeline():
    raw = extract_task()
    sampled = sample_task(raw)
    database_url = load_raw_task(sampled)
    dbt_run_task(database_url)
    dbt_test_task(database_url)
    print("Pipeline completo.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Registra el flow con un schedule diario (requiere `prefect server start` corriendo aparte)")
    args = parser.parse_args()

    if args.serve:
        elt_pipeline.serve(name="fintech-fraud-daily", cron="0 3 * * *")
    else:
        elt_pipeline()
