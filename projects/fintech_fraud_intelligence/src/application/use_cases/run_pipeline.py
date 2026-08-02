"""
Main ETL pipeline: CSV -> clean -> Star Schema -> Postgres.

Every project starts here. See README.md for the dataset download step this
pipeline depends on (data/raw/paysim.csv).
"""

from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine

from src.application.use_cases.transform_star_schema import transform
from src.config import RAW_DATA, ROOT
from src.infrastructure.extractors.csv_extractor import PaySimCsvExtractor
from src.infrastructure.repositories.postgres_repository import PostgresStarSchemaLoader


def run_pipeline() -> None:
    print("Pipeline initialized.")

    # -------------------------------
    # 1. Load data
    # -------------------------------
    extractor = PaySimCsvExtractor(RAW_DATA / "paysim.csv")
    raw = extractor.extract()
    print(f"  extracted {len(raw):,} raw transactions")

    # -------------------------------
    # 2. Clean data + 3. Feature Engineering (Star Schema shaping)
    # -------------------------------
    star_schema = transform(raw)

    # -------------------------------
    # 4. Train / Analyze — descriptive only in this project; see
    #    Data-Analyst-Roadmap/handbook_es/08_Machine_Learning.md for the
    #    optional fraud-classification extension.
    # -------------------------------

    # -------------------------------
    # 5. Export — load the Star Schema into Postgres for SQL (see /sql)
    #    and Power BI (see /powerbi) to consume.
    # -------------------------------
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)
    loader = PostgresStarSchemaLoader(engine)
    loader.load(star_schema)

    print("Pipeline finished.")
