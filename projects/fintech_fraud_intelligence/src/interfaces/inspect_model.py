"""
Opens the "black box": feature importance, a precision/recall-vs-threshold
sweep, and a leakage-ablation comparison (with vs. without the suspicious
balance features flagged in reports/reporte_modelo_fraude.md).

Run:
    python -m src.interfaces.inspect_model
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine
from sklearn.metrics import precision_recall_curve

from src.application.use_cases.train_fraud_model import build_features, train_and_evaluate
from src.config import REPORTS, ROOT

sns.set_theme(style="whitegrid")

SUSPECT_FEATURES = ["origin_balance_delta", "balance_mismatch"]


def load_data(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        fact = pd.read_sql("SELECT * FROM fact_transactions", conn)
        dim_type = pd.read_sql("SELECT * FROM dim_type", conn)
    return build_features(fact, dim_type)


def plot_feature_importance(result: dict) -> pd.DataFrame:
    model = result["pipeline"].named_steps["model"]
    importances = pd.Series(model.feature_importances_, index=result["feature_names"])
    importances = importances.sort_values(ascending=False).head(15)

    plt.figure(figsize=(9, 6))
    sns.barplot(x=importances.values, y=importances.index)
    plt.title("Importancia de features — qué mira el modelo para decidir")
    plt.xlabel("Importancia (Gini)")
    plt.tight_layout()
    plt.savefig(REPORTS / "importancia_features.png", dpi=150)
    plt.close()
    return importances


def plot_threshold_sweep(y_test, y_proba) -> pd.DataFrame:
    precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
    # precision_recall_curve returns one more point than thresholds; align them.
    sweep = pd.DataFrame(
        {"threshold": thresholds, "precision": precision[:-1], "recall": recall[:-1]}
    )
    sample = sweep.iloc[:: max(len(sweep) // 200, 1)]  # thin out for a readable chart

    plt.figure(figsize=(9, 5))
    plt.plot(sample["threshold"], sample["precision"], label="Precision")
    plt.plot(sample["threshold"], sample["recall"], label="Recall")
    plt.xlabel("Umbral de decisión (probabilidad mínima para marcar fraude)")
    plt.ylabel("Score")
    plt.title("Precision y Recall según el umbral elegido")
    plt.legend()
    plt.tight_layout()
    plt.savefig(REPORTS / "barrido_umbral.png", dpi=150)
    plt.close()

    # A few representative rows for the written report.
    checkpoints = sweep.iloc[:: max(len(sweep) // 10, 1)]
    return checkpoints


def compare_with_and_without_leakage(df: pd.DataFrame) -> str:
    full = train_and_evaluate(df, model_name="random_forest")
    ablated = train_and_evaluate(df, model_name="random_forest", exclude_features=SUSPECT_FEATURES)

    auc_drop = full["roc_auc"] - ablated["roc_auc"]
    f1_drop = full["cv_f1_mean"] - ablated["cv_f1_mean"]

    if f1_drop > 0.15 and auc_drop <= 0.02:
        verdict = (
            "**Leakage parcial confirmado, pero no como se esperaba:** el ROC-AUC (capacidad de "
            "*ordenar* fraude vs. no-fraude, sin importar el umbral) casi no cae — el modelo sigue "
            "separando bien usando `type`, `amount` y los balances originales. Pero el F1 en el "
            "umbral por defecto (0.5) se derrumba sin esas dos features, porque las probabilidades "
            "quedan mal calibradas en ese punto exacto sin la señal 'fácil' del balance vaciado. "
            "Conclusión: el modelo 'hacía trampa' para tener un F1 artificialmente alto en el umbral "
            "0.5, aunque su capacidad de separación general no dependiera tanto de esas features."
        )
    elif auc_drop > 0.02:
        verdict = (
            "**Confirmado:** tanto el ROC-AUC como el F1 caen de forma notable sin esas features — "
            "el modelo dependía en gran parte de ese patrón sintético de PaySim, no de una "
            "separación 'real' generalizable."
        )
    else:
        verdict = (
            "**El modelo se mantiene sólido sin esas features** en ambas métricas — la hipótesis de "
            "leakage no explica el resultado, hay otras señales (tipo de transacción, montos) que "
            "también separan bien."
        )

    return f"""## Comparación: con vs. sin features sospechosas de leakage

| | Con {', '.join(SUSPECT_FEATURES)} | Sin esas features |
|---|---|---|
| ROC-AUC | {full['roc_auc']:.4f} | {ablated['roc_auc']:.4f} |
| F1 (CV, 5-fold) | {full['cv_f1_mean']:.4f} | {ablated['cv_f1_mean']:.4f} |

{verdict}
"""


def main() -> None:
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)

    print("Cargando datos y reentrenando (para tener el pipeline en memoria)...")
    df = load_data(engine)
    result = train_and_evaluate(df, model_name="random_forest")

    print("Calculando importancia de features...")
    importances = plot_feature_importance(result)

    print("Calculando barrido de umbral...")
    checkpoints = plot_threshold_sweep(result["y_test"], result["y_proba"])

    print("Comparando con/sin features sospechosas de leakage (esto reentrena 2 modelos más)...")
    comparison = compare_with_and_without_leakage(df)

    report = f"""# Inspección del modelo — fintech_fraud_intelligence

## Top 15 features por importancia
```
{importances.to_string()}
```

## Umbral de decisión: algunos puntos de referencia
```
{checkpoints.to_string(index=False)}
```
Interpretación: en el umbral por defecto (0.5), el modelo prioriza mucho el
recall. Si el costo de negocio de una falsa alarma (molestar a un cliente
legítimo) es alto, conviene subir el umbral — sacrifica algo de recall a
cambio de más precision. Ver `reports/barrido_umbral.png` para la curva
completa.

{comparison}
"""
    (REPORTS / "inspeccion_modelo.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"Gráficos y reporte guardados en {REPORTS}")


if __name__ == "__main__":
    main()
