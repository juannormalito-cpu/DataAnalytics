"""
Calibración de probabilidades: cuando el modelo dice "70% de probabilidad
de fraude", ¿ese 70% realmente significa que 7 de cada 10 casos así
etiquetados son fraude? Un modelo con buen ROC-AUC puede estar mal
calibrado — son propiedades distintas.

Run:
    python -m src.interfaces.calibrate_model
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.model_selection import train_test_split

from src.application.use_cases.train_fraud_model import (
    BOOLEAN_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_features,
    build_pipeline,
)
from src.config import REPORTS, ROOT

sns.set_theme(style="whitegrid")


def load_data(engine) -> pd.DataFrame:
    with engine.connect() as conn:
        fact = pd.read_sql("SELECT * FROM fact_transactions", conn)
        dim_type = pd.read_sql("SELECT * FROM dim_type", conn)
    return build_features(fact, dim_type)


def main() -> None:
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)
    df = load_data(engine)

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES + BOOLEAN_FEATURES]
    y = df["is_fraud"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    print("Entrenando modelo sin calibrar...")
    uncalibrated = build_pipeline("random_forest")
    uncalibrated.fit(X_train, y_train)
    proba_uncalibrated = uncalibrated.predict_proba(X_test)[:, 1]

    print("Calibrando con Platt scaling (sigmoid, cross-validated)...")
    calibrated = CalibratedClassifierCV(build_pipeline("random_forest"), method="sigmoid", cv=3)
    calibrated.fit(X_train, y_train)
    proba_calibrated = calibrated.predict_proba(X_test)[:, 1]

    prob_true_unc, prob_pred_unc = calibration_curve(y_test, proba_uncalibrated, n_bins=10, strategy="quantile")
    prob_true_cal, prob_pred_cal = calibration_curve(y_test, proba_calibrated, n_bins=10, strategy="quantile")

    plt.figure(figsize=(7, 7))
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Calibración perfecta")
    plt.plot(prob_pred_unc, prob_true_unc, marker="o", label="Sin calibrar")
    plt.plot(prob_pred_cal, prob_true_cal, marker="o", label="Calibrado (Platt scaling)")
    plt.xlabel("Probabilidad predicha promedio")
    plt.ylabel("Fracción real de fraude")
    plt.title("Curva de calibración")
    plt.legend()
    plt.tight_layout()
    REPORTS.mkdir(parents=True, exist_ok=True)
    plt.savefig(REPORTS / "calibracion.png", dpi=150)
    plt.close()

    def as_table(pred, true) -> str:
        rows = "\n".join(f"| {p:.3f} | {t:.3f} |" for p, t in zip(pred, true))
        return f"| Probabilidad predicha (bin) | Fracción real de fraude |\n|---|---|\n{rows}"

    report = f"""# Calibración de probabilidades — fintech_fraud_intelligence

## Sin calibrar
{as_table(prob_pred_unc, prob_true_unc)}

## Calibrado (Platt scaling / sigmoid, 3-fold CV)
{as_table(prob_pred_cal, prob_true_cal)}

## Interpretación
Si el modelo estuviera perfectamente calibrado, un bin con probabilidad
predicha promedio de 0.7 debería tener exactamente 70% de casos con fraude
real. Cuanto más cerca de la diagonal en `calibracion.png`, mejor calibrado.

Esto importa para decisiones de negocio: si el equipo de Riesgo va a usar
la probabilidad directamente (ej. "revisar manualmente todo caso con
probabilidad > 60%"), esa probabilidad tiene que significar lo que dice —
no solo servir para *ordenar* casos (que es todo lo que el ROC-AUC mide).
"""
    (REPORTS / "calibracion.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
