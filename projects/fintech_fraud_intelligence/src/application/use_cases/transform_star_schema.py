"""Cleans the raw PaySim export and reshapes it into a Star Schema:
fact_transactions + dim_time + dim_type — the same pattern taught in
Data-Analyst-Roadmap/handbook_es/03_Bases_de_Datos.md (Star Schema) and applied
end-to-end in handbook_es/07_Proyectos_Profesionales.md.

Note on `dim_account`: PaySim's account IDs are almost all one-off (each
account appears in ~1 transaction), so a classic "dimension" table for
accounts wouldn't actually be smaller than the fact table — it defeats the
point of dimensional modeling (dimensions should be small and reused). We
keep account_kind (customer/merchant) as a derived column directly on the
fact table instead of a separate dimension.
"""

import pandas as pd


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df = df.drop_duplicates()
    df["type"] = df["type"].str.upper().str.strip()
    df["isFraud"] = df["isFraud"].astype(bool)
    df["isFlaggedFraud"] = df["isFlaggedFraud"].astype(bool)
    # PaySim's `step` is hours since simulation start (1..744, ~30 days).
    df = df[df["step"].between(1, 744)]
    return df


def sample_for_storage_budget(
    df: pd.DataFrame, non_fraud_sample_size: int = 1_000_000, random_state: int = 42
) -> pd.DataFrame:
    """Keeps every fraud row (rare and valuable — see handbook_es/08_Machine_Learning.md
    §8.4 on class imbalance) and randomly samples the majority (non-fraud) class down
    to a size that fits a free-tier Postgres budget (e.g. Neon's 512MB)."""
    fraud = df[df["isFraud"] == 1]
    non_fraud = df[df["isFraud"] == 0]
    if len(non_fraud) > non_fraud_sample_size:
        non_fraud = non_fraud.sample(n=non_fraud_sample_size, random_state=random_state)
    sampled = pd.concat([fraud, non_fraud]).sort_values("step").reset_index(drop=True)
    print(
        f"  sampled: {len(sampled):,} rows "
        f"({len(fraud):,} fraud + {len(non_fraud):,} non-fraud, "
        f"from {len(df):,} raw)"
    )
    return sampled


def build_dim_time(df: pd.DataFrame) -> pd.DataFrame:
    steps = pd.DataFrame({"step": sorted(df["step"].unique())})
    steps["day"] = ((steps["step"] - 1) // 24) + 1
    steps["hour_of_day"] = (steps["step"] - 1) % 24
    steps["is_weekend_sim"] = (steps["day"] % 7).isin([6, 0])  # synthetic weekly cycle
    return steps.rename(columns={"step": "time_id"})


def build_dim_type(df: pd.DataFrame) -> pd.DataFrame:
    types = pd.DataFrame({"type": sorted(df["type"].unique())})
    types.insert(0, "type_id", range(1, len(types) + 1))
    return types


def _account_kind(account_id: pd.Series) -> pd.Series:
    return account_id.str.slice(0, 1).map({"C": "customer", "M": "merchant"})


def build_fact_transactions(df: pd.DataFrame, dim_type: pd.DataFrame) -> pd.DataFrame:
    fact = df.merge(dim_type, on="type", how="left")
    fact = fact.rename(
        columns={
            "step": "time_id",
            "amount": "amount",
            "nameOrig": "origin_account_id",
            "oldbalanceOrg": "origin_balance_before",
            "newbalanceOrig": "origin_balance_after",
            "nameDest": "dest_account_id",
            "oldbalanceDest": "dest_balance_before",
            "newbalanceDest": "dest_balance_after",
            "isFraud": "is_fraud",
            "isFlaggedFraud": "is_flagged_fraud",
        }
    )
    fact["origin_account_kind"] = _account_kind(fact["origin_account_id"])
    fact["dest_account_kind"] = _account_kind(fact["dest_account_id"])
    fact["balance_mismatch"] = (
        (fact["origin_balance_before"] - fact["amount"] - fact["origin_balance_after"]).abs() > 0.01
    )
    return fact[
        [
            "time_id", "type_id", "amount",
            "origin_account_id", "origin_account_kind",
            "origin_balance_before", "origin_balance_after",
            "dest_account_id", "dest_account_kind",
            "dest_balance_before", "dest_balance_after",
            "is_fraud", "is_flagged_fraud", "balance_mismatch",
        ]
    ]


def transform(raw: pd.DataFrame, non_fraud_sample_size: int = 1_000_000) -> dict[str, pd.DataFrame]:
    df = clean(raw)
    df = sample_for_storage_budget(df, non_fraud_sample_size=non_fraud_sample_size)
    dim_type = build_dim_type(df)
    return {
        "dim_time": build_dim_time(df),
        "dim_type": dim_type,
        "fact_transactions": build_fact_transactions(df, dim_type),
    }
