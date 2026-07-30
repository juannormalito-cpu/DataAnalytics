import sys
from pathlib import Path

from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine
from shared_core.logging.logger import setup_logger

from src.application.use_cases.evaluate_project import evaluate
from src.application.use_cases.ingest_series import run_ingestion
from src.config import LOGS, ROOT
from src.infrastructure.repositories.timeseries_repository import TimeSeriesRepository

USAGE = "Uso: python main.py [ingest|evaluate]"


def print_banner() -> None:
    print("=" * 60)
    print("PROJECT:", Path.cwd().name)
    print("=" * 60)


def cmd_ingest(logger) -> None:
    settings = load_settings(ROOT / ".env")
    engine = get_engine(settings.database_url)
    repository = TimeSeriesRepository(engine)

    logger.info("Ingesta de series iniciada.")
    results = run_ingestion(repository)
    for job_name, count in results.items():
        logger.info(f"{job_name}: {count} observaciones")
    logger.info("Ingesta finalizada.")


def cmd_evaluate(logger) -> None:
    # Flujo de fondos de ejemplo (proyecto genérico a 5 años): reemplazar por un caso real
    # de agricultura/ganadería/forestación cuando haya datos ingeridos para armarlo.
    cash_flows = [-100_000, 25_000, 30_000, 35_000, 35_000, 30_000]
    discount_rate = 0.12

    result = evaluate(cash_flows, discount_rate)
    logger.info(f"VAN: {result.net_present_value:,.2f}")
    logger.info(
        "TIR: "
        + (f"{result.internal_rate_of_return:.2%}" if result.internal_rate_of_return else "N/A")
    )
    logger.info(
        "Payback (años): "
        + (f"{result.payback_period_years:.2f}" if result.payback_period_years else "N/A")
    )
    logger.info(
        "Índice de rentabilidad: "
        + (f"{result.profitability_index:.2f}" if result.profitability_index else "N/A")
    )


def main() -> None:
    logger = setup_logger(LOGS)

    logger.info("Project started.")

    print_banner()

    command = sys.argv[1] if len(sys.argv) > 1 else "ingest"

    try:
        if command == "ingest":
            cmd_ingest(logger)
        elif command == "evaluate":
            cmd_evaluate(logger)
        else:
            print(USAGE)
            return

        logger.info("Project finished successfully.")

    except KeyboardInterrupt:

        logger.warning("Execution interrupted by user.")

    except Exception as e:

        logger.exception(e)

        raise
