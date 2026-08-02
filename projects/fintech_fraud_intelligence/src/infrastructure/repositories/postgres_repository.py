"""Loads the Star Schema DataFrames into Postgres. One responsibility: write, nothing else.

Uses COPY (via psycopg2's raw connection) instead of pandas.to_sql's default
row-by-row INSERTs — for a multi-million-row fact table over a network
connection (e.g. Neon), COPY is roughly 10-50x faster.
"""

import csv
import io

import pandas as pd
from sqlalchemy.engine import Engine

from shared_core.etl.contracts import Loader

TABLE_ORDER = ["dim_time", "dim_type", "fact_transactions"]


def _create_table_from_df(conn, table: str, df: pd.DataFrame) -> None:
    # Let pandas generate the CREATE TABLE (correct types) without inserting rows,
    # then COPY does the actual bulk load.
    df.head(0).to_sql(table, conn, if_exists="replace", index=False)


def _copy_dataframe(raw_conn, table: str, df: pd.DataFrame) -> None:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False, quoting=csv.QUOTE_MINIMAL)
    buffer.seek(0)
    with raw_conn.cursor() as cur:
        columns = ", ".join(f'"{c}"' for c in df.columns)
        cur.copy_expert(
            f'COPY "{table}" ({columns}) FROM STDIN WITH (FORMAT csv)', buffer
        )
    raw_conn.commit()


class PostgresStarSchemaLoader(Loader):
    def __init__(self, engine: Engine, chunk_size: int = 200_000):
        self.engine = engine
        self.chunk_size = chunk_size

    def load(self, data: dict[str, pd.DataFrame]) -> None:
        with self.engine.begin() as conn:
            for table in TABLE_ORDER:
                _create_table_from_df(conn, table, data[table])

        raw_conn = self.engine.raw_connection()
        try:
            for table in TABLE_ORDER:
                df = data[table]
                total = len(df)
                for start in range(0, total, self.chunk_size):
                    chunk = df.iloc[start : start + self.chunk_size]
                    _copy_dataframe(raw_conn, table, chunk)
                    print(f"  {table}: {min(start + self.chunk_size, total):,}/{total:,} rows")
        finally:
            raw_conn.close()
