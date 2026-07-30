"""
Proyección de tendencia: regresión lineal simple sobre una serie anual (año -> valor),
sin leer noticias todavía (eso queda para una fase posterior, ver README). Es
intencionalmente el método más simple posible — sirve para mostrar "hacia dónde viene
la tendencia", no como pronóstico riguroso, y siempre se muestra distinguido de los
datos oficiales.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TrendPoint:
    year: int
    value: float


def project_linear_trend(
    years: list[int], values: list[float], years_ahead: int
) -> list[TrendPoint]:
    """Ajusta una recta por cuadrados mínimos sobre (years, values) y devuelve
    `years_ahead` puntos proyectados a continuación del último año observado."""
    if len(years) < 2:
        return []

    slope, intercept = np.polyfit(years, values, deg=1)
    last_year = max(years)

    return [
        TrendPoint(year=last_year + step, value=float(slope * (last_year + step) + intercept))
        for step in range(1, years_ahead + 1)
    ]
