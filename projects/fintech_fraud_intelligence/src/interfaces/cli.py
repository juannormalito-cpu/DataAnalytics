from pathlib import Path

from shared_core.logging.logger import setup_logger

from src.application.use_cases.run_pipeline import run_pipeline
from src.config import LOGS


def print_banner() -> None:
    print("=" * 60)
    print("PROJECT:", Path.cwd().name)
    print("=" * 60)


def main() -> None:
    logger = setup_logger(LOGS)

    logger.info("Project started.")

    print_banner()

    try:
        run_pipeline()

        logger.info("Project finished successfully.")

    except KeyboardInterrupt:

        logger.warning("Execution interrupted by user.")

    except Exception as e:

        logger.exception(e)

        raise
