"""
Trains a fraud classifier on fact_transactions.

Framing (see handbook_es/08_Machine_Learning.md §8.1): this is a binary
classification problem with extreme class imbalance (fraud is a small
minority even after our majority-class downsampling in the ETL step) — so
model selection and evaluation are built around Precision/Recall/F1/ROC-AUC,
never plain Accuracy (§8.4).
"""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = [
    "amount",
    "origin_balance_before",
    "origin_balance_after",
    "origin_balance_delta",
    "dest_balance_before",
    "dest_balance_after",
]
CATEGORICAL_FEATURES = ["type", "origin_account_kind", "dest_account_kind"]
BOOLEAN_FEATURES = ["balance_mismatch"]
TARGET = "is_fraud"


def build_features(fact: pd.DataFrame, dim_type: pd.DataFrame) -> pd.DataFrame:
    df = fact.merge(dim_type, on="type_id")
    df["origin_balance_delta"] = df["origin_balance_after"] - df["origin_balance_before"]
    return df


def build_pipeline(
    model_name: str = "random_forest",
    numeric_features: list[str] | None = None,
    boolean_features: list[str] | None = None,
) -> Pipeline:
    numeric_features = NUMERIC_FEATURES if numeric_features is None else numeric_features
    boolean_features = BOOLEAN_FEATURES if boolean_features is None else boolean_features
    preprocess = ColumnTransformer(
        [
            ("num", StandardScaler(), numeric_features + boolean_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    if model_name == "logistic_regression":
        model = LogisticRegression(max_iter=1000, class_weight="balanced")
    else:
        model = RandomForestClassifier(
            n_estimators=300, max_depth=12, class_weight="balanced", random_state=42, n_jobs=-1
        )
    return Pipeline([("preprocess", preprocess), ("model", model)])


def get_feature_names(pipe: Pipeline) -> list[str]:
    """Expands the ColumnTransformer's output into readable feature names —
    needed because OneHotEncoder splits each category into its own column."""
    return list(pipe.named_steps["preprocess"].get_feature_names_out())


def train_and_evaluate(
    df: pd.DataFrame,
    model_name: str = "random_forest",
    exclude_features: list[str] | None = None,
) -> dict:
    exclude_features = exclude_features or []
    numeric_features = [f for f in NUMERIC_FEATURES if f not in exclude_features]
    boolean_features = [f for f in BOOLEAN_FEATURES if f not in exclude_features]

    X = df[numeric_features + CATEGORICAL_FEATURES + boolean_features]
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    pipe = build_pipeline(model_name, numeric_features, boolean_features)

    cv_scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="f1")
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]

    return {
        "pipeline": pipe,
        "cv_f1_mean": cv_scores.mean(),
        "cv_f1_std": cv_scores.std(),
        "classification_report": classification_report(y_test, y_pred, digits=4),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "y_test": y_test,
        "y_proba": y_proba,
        "feature_names": get_feature_names(pipe),
    }
