"""
Compares RandomForest vs. LogisticRegression on the same data/split —
same idea as the leakage ablation, but varying the algorithm instead of the
features.

Run:
    python -m src.interfaces.compare_models
"""

import pandas as pd
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine

from src.application.use_cases.train_fraud_model import build_features, train_and_evaluate
from src.config import REPORTS, ROOT


def load_data(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        fact = pd.read_sql("SELECT * FROM fact_transactions", conn)
        dim_type = pd.read_sql("SELECT * FROM dim_type", conn)
    return build_features(fact, dim_type)


def main() -> None:
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)
    df = load_data(engine)

    print("Entrenando Random Forest...")
    rf = train_and_evaluate(df, model_name="random_forest")

    print("Entrenando Logistic Regression...")
    lr = train_and_evaluate(df, model_name="logistic_regression")

    report = f"""# Comparación de algoritmos — fintech_fraud_intelligence

| Métrica | Random Forest | Logistic Regression |
|---|---|---|
| ROC-AUC (test) | {rf['roc_auc']:.4f} | {lr['roc_auc']:.4f} |
| F1 (CV, 5-fold) | {rf['cv_f1_mean']:.4f} (+/- {rf['cv_f1_std']:.4f}) | {lr['cv_f1_mean']:.4f} (+/- {lr['cv_f1_std']:.4f}) |

## Random Forest — classification report
```
{rf['classification_report']}
```

## Logistic Regression — classification report
```
{lr['classification_report']}
```

## Por qué pueden diferir

Random Forest puede capturar **relaciones no lineales** entre features
(ej. "fraude solo si `balance_mismatch=True` Y `type=TRANSFER`" — una
combinación, no una suma ponderada). Logistic Regression solo aprende
**combinaciones lineales** de las features — es más simple, más rápida,
más fácil de explicar ("cada feature suma o resta X puntos de riesgo"), y
en muchos negocios reales se prefiere por eso, aunque pierda algo de
performance frente a un modelo más complejo.
"""
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "comparacion_algoritmos.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
