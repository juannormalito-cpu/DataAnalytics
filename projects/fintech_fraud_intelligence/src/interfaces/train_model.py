"""
Runnable independently of the ETL pipeline: reads fact_transactions from
Postgres, trains a fraud classifier, evaluates it, and saves the model +
a threshold-selection chart to /models and /reports.

Run:
    python -m src.interfaces.train_model
"""

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine
from sklearn.metrics import PrecisionRecallDisplay, RocCurveDisplay

from src.application.use_cases.train_fraud_model import build_features, train_and_evaluate
from src.config import MODELS, REPORTS, ROOT

sns.set_theme(style="whitegrid")


def load_data(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        fact = pd.read_sql("SELECT * FROM fact_transactions", conn)
        dim_type = pd.read_sql("SELECT * FROM dim_type", conn)
    return build_features(fact, dim_type)


def plot_precision_recall_and_roc(y_test, y_proba) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    PrecisionRecallDisplay.from_predictions(y_test, y_proba, ax=axes[0])
    axes[0].set_title("Precision-Recall")
    RocCurveDisplay.from_predictions(y_test, y_proba, ax=axes[1])
    axes[1].set_title("ROC")
    plt.tight_layout()
    plt.savefig(REPORTS / "modelo_fraude_curvas.png", dpi=150)
    plt.close()


def write_report(result: dict) -> None:
    report = f"""# Reporte del modelo de fraude — fintech_fraud_intelligence

## Validación cruzada (5-fold, train set)
F1 promedio: {result['cv_f1_mean']:.4f} (+/- {result['cv_f1_std']:.4f})

## Evaluación en test set (hold-out, 20%)
ROC-AUC: {result['roc_auc']:.4f}

```
{result['classification_report']}
```

## Matriz de confusión (test set)
```
{result['confusion_matrix']}
```

## Nota sobre el dataset
Este modelo entrena sobre el dataset muestreado (ver README.md del proyecto):
se conservó el 100% del fraude real y se muestreó la clase mayoritaria a 1M
de filas. Esto NO es la tasa de fraude real de PaySim (~0.13%) sino una
aproximada al 0.81% — el modelo generaliza sobre el patrón, pero cualquier
métrica de "fraude detectado en producción" debería recalibrarse contra el
volumen real antes de usarse para decisiones de negocio.
"""
    (REPORTS / "reporte_modelo_fraude.md").write_text(report, encoding="utf-8")
    print(report)


def main() -> None:
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)

    print("Cargando datos...")
    df = load_data(engine)

    print("Entrenando modelo (Random Forest, class_weight=balanced)...")
    result = train_and_evaluate(df, model_name="random_forest")

    MODELS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    joblib.dump(result["pipeline"], MODELS / "fraud_classifier.joblib")
    print(f"Modelo guardado en {MODELS / 'fraud_classifier.joblib'}")

    plot_precision_recall_and_roc(result["y_test"], result["y_proba"])
    write_report(result)
    print(f"Reporte y gráficos guardados en {REPORTS}")


if __name__ == "__main__":
    main()
