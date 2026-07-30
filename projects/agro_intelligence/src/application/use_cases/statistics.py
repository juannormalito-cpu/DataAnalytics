"""Estadísticas descriptivas sobre una serie de observaciones: media, mediana, desvío
estándar, mínimo, máximo y coeficiente de variación (volatilidad relativa — útil para
comparar qué tan estable es el precio/rendimiento de un cultivo frente a otro)."""

import statistics
from dataclasses import dataclass

from src.domain.timeseries import Observation


@dataclass(frozen=True)
class SeriesStatistics:
    count: int
    mean: float
    median: float
    std_dev: float
    minimum: float
    maximum: float
    coefficient_of_variation: float | None  # std_dev / mean, en %; None si mean == 0


def describe_stats(observations: list[Observation]) -> SeriesStatistics | None:
    if not observations:
        return None

    values = [observation.value for observation in observations]
    mean = statistics.fmean(values)
    std_dev = statistics.stdev(values) if len(values) > 1 else 0.0

    return SeriesStatistics(
        count=len(values),
        mean=mean,
        median=statistics.median(values),
        std_dev=std_dev,
        minimum=min(values),
        maximum=max(values),
        coefficient_of_variation=(std_dev / mean * 100) if mean != 0 else None,
    )
