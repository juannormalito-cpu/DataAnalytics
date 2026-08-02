"""
Serves the fraud model as an HTTP API — the concrete step from "trained
model file" to "something a real application could call." This is the
ML Engineer handoff described in handbook_es/08_Machine_Learning.md §8.6.

Serves two models:
  - /score          the full model (higher metrics, but see reports/reporte_modelo_fraude.md
                     for the leakage caveat — it leans on a PaySim-specific balance pattern)
  - /score/honest    the same model retrained without the two suspicious features
                     (src/interfaces/train_honest_model.py) — the more realistic
                     candidate if this were ever pointed at real transaction data

Run:
    uvicorn src.interfaces.api:app --reload --port 8000

Then, e.g.:
    curl -X POST http://localhost:8000/score -H "Content-Type: application/json" -d '{
      "amount": 181, "type": "TRANSFER",
      "origin_balance_before": 181, "origin_balance_after": 0,
      "dest_balance_before": 0, "dest_balance_after": 0,
      "origin_account_kind": "customer", "dest_account_kind": "customer"
    }'
"""

from contextlib import asynccontextmanager
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.config import MODELS

MODEL_STATE: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    full_path = MODELS / "fraud_classifier.joblib"
    honest_path = MODELS / "fraud_classifier_honest.joblib"

    if not full_path.exists():
        raise RuntimeError(f"No hay modelo en {full_path}. Corré: python -m src.interfaces.train_model")
    MODEL_STATE["full"] = joblib.load(full_path)
    print(f"Modelo completo cargado desde {full_path}")

    if honest_path.exists():
        MODEL_STATE["honest"] = joblib.load(honest_path)
        print(f"Modelo honesto cargado desde {honest_path}")
    else:
        print(f"  (opcional) no se encontró {honest_path} — /score/honest no va a estar disponible. "
              "Corré: python -m src.interfaces.train_honest_model")

    yield
    MODEL_STATE.clear()


app = FastAPI(
    title="fintech_fraud_intelligence — Fraud Scoring API",
    description="Sirve el clasificador de fraude entrenado sobre PaySim. Ver README.md del proyecto.",
    version="0.2.0",
    lifespan=lifespan,
)


class Transaction(BaseModel):
    amount: float = Field(..., gt=0, description="Monto de la transacción")
    type: Literal["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]
    origin_balance_before: float = Field(..., ge=0)
    origin_balance_after: float = Field(..., ge=0)
    dest_balance_before: float = Field(0, ge=0)
    dest_balance_after: float = Field(0, ge=0)
    origin_account_kind: Literal["customer", "merchant"] = "customer"
    dest_account_kind: Literal["customer", "merchant"] = "customer"


class ScoreResponse(BaseModel):
    fraud_probability: float
    is_fraud_prediction: bool
    threshold_used: float
    model_used: str


def build_row(t: Transaction) -> pd.DataFrame:
    row = t.model_dump()
    row["origin_balance_delta"] = row["origin_balance_after"] - row["origin_balance_before"]
    row["balance_mismatch"] = (
        abs(row["origin_balance_before"] - row["amount"] - row["origin_balance_after"]) > 0.01
    )
    return pd.DataFrame([row])


def _score_with(model_key: str, transaction: Transaction, threshold: float) -> ScoreResponse:
    pipe = MODEL_STATE.get(model_key)
    if pipe is None:
        raise HTTPException(status_code=503, detail=f"Modelo '{model_key}' no disponible")

    row = build_row(transaction)
    proba = float(pipe.predict_proba(row)[0, 1])

    return ScoreResponse(
        fraud_probability=proba,
        is_fraud_prediction=proba >= threshold,
        threshold_used=threshold,
        model_used=model_key,
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "models_loaded": {"full": "full" in MODEL_STATE, "honest": "honest" in MODEL_STATE},
    }


@app.post("/score", response_model=ScoreResponse)
def score(transaction: Transaction, threshold: float = 0.5):
    """Modelo completo — mejores métricas, pero ver la nota de leakage en el README."""
    return _score_with("full", transaction, threshold)


@app.post("/score/honest", response_model=ScoreResponse)
def score_honest(transaction: Transaction, threshold: float = 0.5):
    """Modelo sin origin_balance_delta/balance_mismatch — el candidato más
    realista si esto se apuntara a datos de transacciones reales."""
    return _score_with("honest", transaction, threshold)
