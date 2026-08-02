"""
Explains individual predictions with SHAP — not "what does the model care
about in general" (that's feature importance, Part 7 of the manual) but
"why did the model predict THIS for THIS specific transaction."

Run:
    python -m src.interfaces.explain_predictions
"""

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine

from src.application.use_cases.train_fraud_model import (
    BOOLEAN_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_features,
)
from src.config import MODELS, REPORTS, ROOT


def load_sample(engine, n_fraud: int = 3, n_normal: int = 3) -> pd.DataFrame:
    with engine.connect() as conn:
        fact = pd.read_sql("SELECT * FROM fact_transactions", conn)
        dim_type = pd.read_sql("SELECT * FROM dim_type", conn)
    df = build_features(fact, dim_type)
    fraud_sample = df[df["is_fraud"]].sample(n_fraud, random_state=1)
    normal_sample = df[~df["is_fraud"]].sample(n_normal, random_state=1)
    return pd.concat([fraud_sample, normal_sample]).reset_index(drop=True)


def explain(pipe, X: pd.DataFrame):
    preprocess = pipe.named_steps["preprocess"]
    model = pipe.named_steps["model"]

    X_transformed = preprocess.transform(X)
    if hasattr(X_transformed, "toarray"):
        X_transformed = X_transformed.toarray()
    feature_names = list(preprocess.get_feature_names_out())

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_transformed)
    # For a binary RandomForestClassifier, shap_values is [class_0, class_1] — keep class 1 (fraud).
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    elif shap_values.ndim == 3:
        shap_values = shap_values[:, :, 1]

    return shap_values, feature_names, X_transformed


def plot_summary(shap_values, feature_names, X_transformed) -> None:
    plt.figure(figsize=(9, 6))
    shap.summary_plot(
        shap_values, X_transformed, feature_names=feature_names, show=False, max_display=12
    )
    plt.tight_layout()
    plt.savefig(REPORTS / "shap_summary.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_individual_cases(shap_values, feature_names, X_raw, X_transformed, labels) -> str:
    """Waterfall-style bar chart per case: which features pushed the prediction
    toward fraud (positive) vs. away from it (negative)."""
    lines = []
    fig, axes = plt.subplots(len(X_raw), 1, figsize=(9, 3.2 * len(X_raw)))
    if len(X_raw) == 1:
        axes = [axes]

    for i, ax in enumerate(axes):
        row_shap = pd.Series(shap_values[i], index=feature_names).sort_values(key=abs, ascending=False).head(8)
        colors = ["#dc2626" if v > 0 else "#16a34a" for v in row_shap.values]
        ax.barh(row_shap.index[::-1], row_shap.values[::-1], color=colors[::-1])
        ax.set_title(f"Caso {i + 1}: {labels[i]} — top 8 features que más influyeron")
        ax.axvline(0, color="#94a3b8", linewidth=0.8)

        lines.append(f"### Caso {i + 1}: {labels[i]}")
        lines.append(f"amount={X_raw.iloc[i]['amount']:.2f}, type={X_raw.iloc[i]['type']}, "
                      f"origin_balance_delta={X_raw.iloc[i]['origin_balance_delta']:.2f}, "
                      f"balance_mismatch={X_raw.iloc[i]['balance_mismatch']}")
        for feat, val in row_shap.items():
            direction = "empuja hacia FRAUDE" if val > 0 else "empuja hacia NO fraude"
            lines.append(f"- `{feat}`: {val:+.4f} ({direction})")
        lines.append("")

    plt.tight_layout()
    plt.savefig(REPORTS / "shap_casos_individuales.png", dpi=150)
    plt.close()
    return "\n".join(lines)


def main() -> None:
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)
    model_path = MODELS / "fraud_classifier.joblib"
    if not model_path.exists():
        raise SystemExit("Corré primero: python -m src.interfaces.train_model")

    pipe = joblib.load(model_path)

    print("Cargando muestra de casos (fraude + normales)...")
    sample = load_sample(engine)
    X = sample[NUMERIC_FEATURES + CATEGORICAL_FEATURES + BOOLEAN_FEATURES]
    labels = ["FRAUDE real" if f else "no-fraude real" for f in sample["is_fraud"]]

    print("Calculando SHAP values...")
    shap_values, feature_names, X_transformed = explain(pipe, X)

    print("Generando gráfico resumen...")
    plot_summary(shap_values, feature_names, X_transformed)

    print("Generando gráficos por caso individual...")
    case_details = plot_individual_cases(shap_values, feature_names, X, X_transformed, labels)

    report = f"""# Explicabilidad con SHAP — fintech_fraud_intelligence

## Resumen general
Ver `shap_summary.png` — cada punto es una transacción del set de muestra;
el color indica si esa feature era alta (rojo) o baja (azul) para esa
transacción, y la posición horizontal indica si empujó la predicción hacia
fraude (derecha) o no-fraude (izquierda).

## Casos individuales
Ver `shap_casos_individuales.png` para el gráfico. Detalle:

{case_details}
"""
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "shap_explicabilidad.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"Reporte y gráficos guardados en {REPORTS}")


if __name__ == "__main__":
    main()
