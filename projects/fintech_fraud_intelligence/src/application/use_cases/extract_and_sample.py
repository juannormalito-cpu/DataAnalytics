"""
Extract + Sample only — no Star Schema reshaping here anymore. That logic
moved to dbt (see /dbt), following the ELT pattern: land raw data first,
transform inside the warehouse with versioned, tested SQL.

This keeps only what genuinely belongs in Python: reading the CSV and the
class-imbalance-aware sampling decision (a business/ML rule, not a SQL
transformation).
"""

import pandas as pd

from src.application.use_cases.transform_star_schema import clean, sample_for_storage_budget


def extract_and_sample(raw: pd.DataFrame, non_fraud_sample_size: int = 1_000_000) -> pd.DataFrame:
    df = clean(raw)
    df = sample_for_storage_budget(df, non_fraud_sample_size=non_fraud_sample_size)
    return df
