"""
Simula streaming: reproduce transacciones de la base como si fueran eventos
llegando uno por uno en tiempo real, llamando a la API en vivo — la forma
más honesta de sentir cómo se comportaría esto conectado a una app real,
sin necesitar Kafka/infraestructura de streaming de verdad.

Requiere la API corriendo (otra terminal):
    uvicorn src.interfaces.api:app --port 8000

Run:
    python -m src.interfaces.simulate_stream --n 30 --delay 0.5
"""

import argparse
import time

import httpx
import pandas as pd
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine

from src.config import ROOT

API_URL = "http://localhost:8000/score"


def load_sample(engine, n: int) -> pd.DataFrame:
    query = f"""
        SELECT * FROM (
            (SELECT * FROM fact_transactions WHERE is_fraud ORDER BY random() LIMIT {n // 3})
            UNION ALL
            (SELECT * FROM fact_transactions WHERE NOT is_fraud ORDER BY random() LIMIT {n - n // 3})
        ) mixed
        ORDER BY random()
    """
    with engine.connect() as conn:
        return pd.read_sql(query, conn)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=20, help="Cantidad de transacciones a simular")
    parser.add_argument("--delay", type=float, default=0.6, help="Segundos entre eventos")
    args = parser.parse_args()

    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)

    with engine.connect() as conn:
        dim_type = pd.read_sql("SELECT * FROM dim_type", conn)
    type_lookup = dict(zip(dim_type["type_id"], dim_type["type"]))

    print(f"Cargando {args.n} transacciones de muestra (mezcla de fraude y no-fraude)...")
    sample = load_sample(engine, args.n)

    print(f"Simulando {len(sample)} eventos, uno cada {args.delay}s. Ctrl+C para cortar.\n")
    aciertos = 0
    with httpx.Client(timeout=5.0) as client:
        for i, row in sample.iterrows():
            payload = {
                "amount": float(row["amount"]),
                "type": type_lookup[row["type_id"]],
                "origin_balance_before": float(row["origin_balance_before"]),
                "origin_balance_after": float(row["origin_balance_after"]),
                "dest_balance_before": float(row["dest_balance_before"]),
                "dest_balance_after": float(row["dest_balance_after"]),
                "origin_account_kind": row["origin_account_kind"],
                "dest_account_kind": row["dest_account_kind"],
            }
            try:
                resp = client.post(API_URL, json=payload)
                resp.raise_for_status()
                result = resp.json()
            except httpx.ConnectError:
                raise SystemExit(
                    "No se pudo conectar a la API. Corré primero: "
                    "uvicorn src.interfaces.api:app --port 8000"
                )

            real = "FRAUDE" if row["is_fraud"] else "normal"
            pred = "FRAUDE" if result["is_fraud_prediction"] else "normal"
            acerto = (pred == "FRAUDE") == bool(row["is_fraud"])
            match = "OK" if acerto else "MISS"
            if acerto:
                aciertos += 1

            tx_type = type_lookup[row["type_id"]]
            print(
                f"[{i+1:>3}] {tx_type:<10} "
                f"monto=${row['amount']:>12,.2f}  real={real:<7}  "
                f"modelo={pred:<7} (p={result['fraud_probability']:.4f})  {match}"
            )
            time.sleep(args.delay)

    print(f"\nAciertos: {aciertos}/{len(sample)} ({100*aciertos/len(sample):.1f}%)")


if __name__ == "__main__":
    main()
