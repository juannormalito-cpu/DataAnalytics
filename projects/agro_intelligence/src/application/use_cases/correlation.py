"""Cruce entre dos series: promedio anual de cada una + correlación de Pearson sobre
los años en común. Sirve para preguntas del tipo "¿el tipo de cambio se relaciona con
el rendimiento de soja?" sin necesitar que las dos series tengan la misma frecuencia."""

import pandas as pd

from src.domain.timeseries import Observation


def to_annual_series(observations: list[Observation]) -> pd.Series:
    if not observations:
        return pd.Series(dtype=float)

    frame = pd.DataFrame(
        {
            "year": [observation.date.year for observation in observations],
            "value": [observation.value for observation in observations],
        }
    )
    return frame.groupby("year")["value"].mean()


def correlate(
    observations_a: list[Observation], observations_b: list[Observation]
) -> float | None:
    series_a = to_annual_series(observations_a)
    series_b = to_annual_series(observations_b)

    merged = pd.concat([series_a, series_b], axis=1, join="inner")
    if len(merged) < 3:
        return None

    return float(merged.iloc[:, 0].corr(merged.iloc[:, 1]))


def correlation_matrix(observations_by_label: dict[str, list[Observation]]) -> pd.DataFrame:
    """Correlación de a pares entre todas las variables recibidas, cada una resuelta a su
    propio promedio anual (cada par usa sus propios años en común, no una tabla única)."""
    labels = list(observations_by_label)
    annual_series = {label: to_annual_series(obs) for label, obs in observations_by_label.items()}

    matrix = pd.DataFrame(index=labels, columns=labels, dtype=float)
    for label_a in labels:
        for label_b in labels:
            if label_a == label_b:
                matrix.loc[label_a, label_b] = 1.0
                continue

            merged = pd.concat(
                [annual_series[label_a], annual_series[label_b]], axis=1, join="inner"
            )
            matrix.loc[label_a, label_b] = (
                merged.iloc[:, 0].corr(merged.iloc[:, 1]) if len(merged) >= 3 else float("nan")
            )

    return matrix
