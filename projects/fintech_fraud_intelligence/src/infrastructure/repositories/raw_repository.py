"""Loads the sampled-but-untransformed data into a `raw_transactions` table —
the "L" in ELT. dbt takes it from here (see /dbt/models)."""

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.infrastructure.repositories.postgres_repository import _copy_dataframe, _create_table_from_df


class RawTransactionsLoader:
    def __init__(self, engine: Engine, chunk_size: int = 200_000):
        self.engine = engine
        self.chunk_size = chunk_size

    def load(self, df: pd.DataFrame) -> None:
        with self.engine.begin() as conn:
            # CASCADE porque dbt crea stg_transactions (una vista) encima de
            # esta tabla — un DROP simple falla en la segunda corrida.
            conn.execute(text("DROP TABLE IF EXISTS raw_transactions CASCADE"))
            _create_table_from_df(conn, "raw_transactions", df)

        raw_conn = self.engine.raw_connection()
        try:
            total = len(df)
            for start in range(0, total, self.chunk_size):
                chunk = df.iloc[start : start + self.chunk_size]
                _copy_dataframe(raw_conn, "raw_transactions", chunk)
                print(f"  raw_transactions: {min(start + self.chunk_size, total):,}/{total:,} filas")
        finally:
            raw_conn.close()
