"""
Entrena y guarda el modelo "honesto" — sin origin_balance_delta ni
balance_mismatch, las features sospechosas de leakage (ver reports/reporte_modelo_fraude.md
e inspeccion_modelo.md). Este es el modelo que tiene más sentido llevar a
producción si algún día se usan datos reales, no solo PaySim.

Run:
    python -m src.interfaces.train_honest_model
"""

import joblib
import pandas as pd
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine

from src.application.use_cases.train_fraud_model import build_features, train_and_evaluate
from src.config import MODELS, REPORTS, ROOT

SUSPECT_FEATURES = ["origin_balance_delta", "balance_mismatch"]


def load_data(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        fact = pd.read_sql("SELECT * FROM fact_transactions", conn)
        dim_type = pd.read_sql("SELECT * FROM dim_type", conn)
    return build_features(fact, dim_type)


def main() -> None:
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)
    df = load_data(engine)

    print("Entrenando modelo honesto (sin features de leakage)...")
    result = train_and_evaluate(df, model_name="random_forest", exclude_features=SUSPECT_FEATURES)

    MODELS.mkdir(parents=True, exist_ok=True)
    joblib.dump(result["pipeline"], MODELS / "fraud_classifier_honest.joblib")

    report = f"""# Modelo honesto — fintech_fraud_intelligence

Excluye: {', '.join(SUSPECT_FEATURES)}

- ROC-AUC (test): {result['roc_auc']:.4f}
- F1 (CV, 5-fold): {result['cv_f1_mean']:.4f} (+/- {result['cv_f1_std']:.4f})

```
{result['classification_report']}
```

Guardado en models/fraud_classifier_honest.joblib — servido en la API bajo
`/score/honest` (ver api.py), como alternativa al modelo completo en `/score`.
"""
    (REPORTS / "modelo_honesto.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
