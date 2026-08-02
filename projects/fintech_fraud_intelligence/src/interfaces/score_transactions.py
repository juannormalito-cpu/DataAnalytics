"""
Batch scoring: runs the trained model over every transaction already in
Postgres and writes the fraud probability back as a new table
(`fraud_scores`), joinable to `fact_transactions` — so Power BI/SQL can show
the model's risk score, not just historical fraud flags.

Adds a surrogate key (`transaction_id`) to `fact_transactions` if it doesn't
exist yet, since the table has no natural primary key.

Run:
    python -m src.interfaces.score_transactions
"""

import joblib
import pandas as pd
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine
from sqlalchemy import text

from src.application.use_cases.train_fraud_model import (
    BOOLEAN_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_features,
)
from src.config import MODELS, ROOT
from src.infrastructure.repositories.postgres_repository import _copy_dataframe, _create_table_from_df


def ensure_surrogate_key(engine) -> None:
    with engine.begin() as conn:
        exists = conn.execute(
            text(
                "SELECT 1 FROM information_schema.columns "
                "WHERE table_name = 'fact_transactions' AND column_name = 'transaction_id'"
            )
        ).fetchone()
        if not exists:
            conn.execute(text("ALTER TABLE fact_transactions ADD COLUMN transaction_id SERIAL"))
            conn.execute(
                text("ALTER TABLE fact_transactions ADD PRIMARY KEY (transaction_id)")
            )
            print("  agregada columna transaction_id (surrogate key) a fact_transactions")


def load_data(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        fact = pd.read_sql("SELECT * FROM fact_transactions", conn)
        dim_type = pd.read_sql("SELECT * FROM dim_type", conn)
    return build_features(fact, dim_type)


def score(pipe, df: pd.DataFrame) -> pd.DataFrame:
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES + BOOLEAN_FEATURES]
    proba = pipe.predict_proba(X)[:, 1]
    return pd.DataFrame(
        {
            "transaction_id": df["transaction_id"],
            "fraud_probability": proba,
            "model_flag": (proba >= 0.5).astype(bool),
        }
    )


def write_scores(engine, scores: pd.DataFrame, chunk_size: int = 200_000) -> None:
    with engine.begin() as conn:
        _create_table_from_df(conn, "fraud_scores", scores)

    raw_conn = engine.raw_connection()
    try:
        total = len(scores)
        for start in range(0, total, chunk_size):
            chunk = scores.iloc[start : start + chunk_size]
            _copy_dataframe(raw_conn, "fraud_scores", chunk)
            print(f"  fraud_scores: {min(start + chunk_size, total):,}/{total:,} filas")
    finally:
        raw_conn.close()


def main() -> None:
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)

    model_path = MODELS / "fraud_classifier.joblib"
    if not model_path.exists():
        raise SystemExit("Corré primero: python -m src.interfaces.train_model")
    pipe = joblib.load(model_path)

    print("Asegurando clave surrogate en fact_transactions...")
    ensure_surrogate_key(engine)

    print("Cargando transacciones...")
    df = load_data(engine)

    print(f"Scoreando {len(df):,} transacciones...")
    scores = score(pipe, df)

    print("Escribiendo fraud_scores en Postgres (COPY)...")
    write_scores(engine, scores)

    high_risk = (scores["fraud_probability"] >= 0.5).sum()
    print(f"\nListo. {high_risk:,} transacciones marcadas de alto riesgo (>= 50% probabilidad).")
    print("Tabla 'fraud_scores' disponible para join en SQL/Power BI vía transaction_id.")


if __name__ == "__main__":
    main()
