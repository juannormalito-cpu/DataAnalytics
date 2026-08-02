"""
EDA runnable independently of the ETL pipeline: reads the Star Schema back
from Postgres and produces charts + a written report in /reports.

Run:
    python -m src.interfaces.eda_report
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from shared_core.config.settings import load_settings
from shared_core.database.engine import get_engine

from src.config import REPORTS, ROOT

sns.set_theme(style="whitegrid")


def load_tables(engine) -> dict[str, pd.DataFrame]:
    with engine.connect() as conn:
        return {
            "fact": pd.read_sql("SELECT * FROM fact_transactions", conn),
            "dim_time": pd.read_sql("SELECT * FROM dim_time", conn),
            "dim_type": pd.read_sql("SELECT * FROM dim_type", conn),
        }


def plot_volume_by_type(fact: pd.DataFrame, dim_type: pd.DataFrame) -> None:
    merged = fact.merge(dim_type, on="type_id")
    counts = merged["type"].value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=counts.index, y=counts.values)
    plt.title("Volumen de transacciones por tipo")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.savefig(REPORTS / "volumen_por_tipo.png", dpi=150)
    plt.close()


def plot_fraud_rate_by_type(fact: pd.DataFrame, dim_type: pd.DataFrame) -> None:
    merged = fact.merge(dim_type, on="type_id")
    rate = merged.groupby("type")["is_fraud"].mean().sort_values(ascending=False) * 100
    plt.figure(figsize=(8, 5))
    sns.barplot(x=rate.index, y=rate.values)
    plt.title("Tasa de fraude por tipo (%)")
    plt.ylabel("% fraude")
    plt.tight_layout()
    plt.savefig(REPORTS / "tasa_fraude_por_tipo.png", dpi=150)
    plt.close()


def plot_daily_trend(fact: pd.DataFrame, dim_time: pd.DataFrame) -> None:
    merged = fact.merge(dim_time, on="time_id")
    daily = merged.groupby("day")["amount"].sum()
    plt.figure(figsize=(10, 5))
    daily.plot()
    plt.title("Monto total movido por día (30 días simulados)")
    plt.ylabel("Monto")
    plt.xlabel("Día")
    plt.tight_layout()
    plt.savefig(REPORTS / "tendencia_diaria.png", dpi=150)
    plt.close()


def write_summary(fact: pd.DataFrame) -> None:
    total = len(fact)
    fraud = fact["is_fraud"].sum()
    fraud_amount = fact.loc[fact["is_fraud"], "amount"].sum()
    mismatches = fact["balance_mismatch"].sum()

    summary = f"""# Resumen EDA — fintech_fraud_intelligence

- Transacciones totales: {total:,}
- Transacciones fraudulentas: {fraud:,} ({fraud / total:.4%})
- Monto total en fraude: {fraud_amount:,.2f}
- Transacciones con inconsistencia de balance: {mismatches:,}

Gráficos generados: volumen_por_tipo.png, tasa_fraude_por_tipo.png, tendencia_diaria.png
"""
    (REPORTS / "resumen_eda.md").write_text(summary, encoding="utf-8")
    print(summary)


def main() -> None:
    settings = load_settings(env_file=ROOT / ".env")
    engine = get_engine(settings.database_url)
    tables = load_tables(engine)

    REPORTS.mkdir(parents=True, exist_ok=True)
    plot_volume_by_type(tables["fact"], tables["dim_type"])
    plot_fraud_rate_by_type(tables["fact"], tables["dim_type"])
    plot_daily_trend(tables["fact"], tables["dim_time"])
    write_summary(tables["fact"])
    print(f"Reporte guardado en {REPORTS}")


if __name__ == "__main__":
    main()
