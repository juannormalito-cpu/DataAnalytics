"""
Score a single, hand-built transaction against the saved model — the fastest
way to build intuition for how the model reacts to different inputs.

Run with defaults (a suspicious TRANSFER that empties the account):
    python -m src.interfaces.predict

Or override any field:
    python -m src.interfaces.predict --amount 5000 --type PAYMENT --origin_balance_before 10000 --origin_balance_after 5000
"""

import argparse

import joblib
import pandas as pd

from src.config import MODELS

DEFAULTS = {
    "amount": 181.0,
    "origin_balance_before": 181.0,
    "origin_balance_after": 0.0,
    "dest_balance_before": 0.0,
    "dest_balance_after": 0.0,
    "type": "TRANSFER",
    "origin_account_kind": "customer",
    "dest_account_kind": "customer",
}


def build_transaction(args: argparse.Namespace) -> pd.DataFrame:
    values = {**DEFAULTS, **{k: v for k, v in vars(args).items() if v is not None}}
    values["origin_balance_delta"] = values["origin_balance_after"] - values["origin_balance_before"]
    values["balance_mismatch"] = (
        abs(values["origin_balance_before"] - values["amount"] - values["origin_balance_after"]) > 0.01
    )
    return pd.DataFrame([values])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", type=float)
    parser.add_argument("--origin_balance_before", type=float)
    parser.add_argument("--origin_balance_after", type=float)
    parser.add_argument("--dest_balance_before", type=float)
    parser.add_argument("--dest_balance_after", type=float)
    parser.add_argument("--type", choices=["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"])
    parser.add_argument("--origin_account_kind", choices=["customer", "merchant"])
    parser.add_argument("--dest_account_kind", choices=["customer", "merchant"])
    args = parser.parse_args()

    model_path = MODELS / "fraud_classifier.joblib"
    if not model_path.exists():
        raise SystemExit(f"No hay modelo guardado en {model_path}. Corré primero: python -m src.interfaces.train_model")

    pipe = joblib.load(model_path)
    transaction = build_transaction(args)

    proba = pipe.predict_proba(transaction)[0, 1]
    pred = pipe.predict(transaction)[0]

    print("Transacción evaluada:")
    print(transaction.to_string(index=False))
    print()
    print(f"Probabilidad de fraude: {proba:.4%}")
    print(f"Predicción (umbral 0.5): {'FRAUDE' if pred else 'no fraude'}")


if __name__ == "__main__":
    main()
