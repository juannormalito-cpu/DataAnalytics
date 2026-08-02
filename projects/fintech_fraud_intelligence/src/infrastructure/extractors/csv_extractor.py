"""Extracts the raw PaySim CSV into a DataFrame. See README.md 'Dataset' section for the
download link — Kaggle requires an account, so it's not auto-downloaded here."""

from pathlib import Path

import pandas as pd

from shared_core.etl.contracts import Extractor

RAW_COLUMNS = [
    "step", "type", "amount",
    "nameOrig", "oldbalanceOrg", "newbalanceOrig",
    "nameDest", "oldbalanceDest", "newbalanceDest",
    "isFraud", "isFlaggedFraud",
]


class PaySimCsvExtractor(Extractor):
    def __init__(self, path: Path):
        self.path = path

    def extract(self) -> pd.DataFrame:
        if not self.path.exists():
            raise FileNotFoundError(
                f"{self.path} not found. Download PaySim from Kaggle "
                "(ealaxi/paysim1) and place it at data/raw/paysim.csv — see README.md."
            )
        df = pd.read_csv(self.path, usecols=RAW_COLUMNS)
        return df
