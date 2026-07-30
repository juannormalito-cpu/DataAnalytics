"""
Comparativa anual entre cultivos.

`compute_gross_revenue` es la comparación real: rendimiento (kg/ha) x precio
internacional de referencia (USD/ton) = ingreso bruto en USD/ha. Es ingreso, no margen
neto — no hay una serie completa de costo de producción (insumos, labores, flete), solo
precio de urea — así que no se resta ningún costo acá; eso queda documentado, no oculto.

`compute_relative_performance` es el proxy anterior (solo rendimiento, sin precio) y se
mantiene como fallback para cuando no hay precio disponible para un cultivo/vertical.
"""

from dataclasses import dataclass

from src.domain.timeseries import Observation


def _annual_average(observations: list[Observation]) -> dict[int, float]:
    by_year: dict[int, list[float]] = {}
    for observation in observations:
        by_year.setdefault(observation.date.year, []).append(observation.value)
    return {year: sum(values) / len(values) for year, values in by_year.items()}


@dataclass(frozen=True)
class YearlyPerformance:
    year: int
    crop: str
    relative_performance: float  # 1.0 = promedio histórico del cultivo; 1.15 = 15% por encima


def compute_relative_performance(
    observations_by_crop: dict[str, list[Observation]],
) -> list[YearlyPerformance]:
    results: list[YearlyPerformance] = []

    for crop, observations in observations_by_crop.items():
        yearly_averages = _annual_average(observations)
        if not yearly_averages:
            continue

        historical_average = sum(yearly_averages.values()) / len(yearly_averages)
        if historical_average == 0:
            continue

        for year, average in yearly_averages.items():
            results.append(
                YearlyPerformance(
                    year=year, crop=crop, relative_performance=average / historical_average
                )
            )

    return results


def best_crop_by_year(performances: list[YearlyPerformance]) -> dict[int, str]:
    best: dict[int, YearlyPerformance] = {}
    for performance in performances:
        current_best = best.get(performance.year)
        is_better = (
            current_best is None
            or performance.relative_performance > current_best.relative_performance
        )
        if is_better:
            best[performance.year] = performance

    return {year: performance.crop for year, performance in best.items()}


@dataclass(frozen=True)
class YearlyRevenue:
    year: int
    crop: str
    revenue_usd_per_ha: float


def compute_gross_revenue(
    yields_by_crop: dict[str, list[Observation]],
    prices_by_crop: dict[str, list[Observation]],
) -> list[YearlyRevenue]:
    results: list[YearlyRevenue] = []

    for crop, yield_observations in yields_by_crop.items():
        price_observations = prices_by_crop.get(crop)
        if not price_observations:
            continue

        yearly_yield = _annual_average(yield_observations)  # kg/ha
        yearly_price = _annual_average(price_observations)  # USD/ton

        for year, yield_value in yearly_yield.items():
            price_value = yearly_price.get(year)
            if price_value is None:
                continue

            results.append(
                YearlyRevenue(
                    year=year,
                    crop=crop,
                    revenue_usd_per_ha=(yield_value / 1000) * price_value,
                )
            )

    return results


def best_crop_by_revenue(revenues: list[YearlyRevenue]) -> dict[int, str]:
    best: dict[int, YearlyRevenue] = {}
    for revenue in revenues:
        current_best = best.get(revenue.year)
        is_better = (
            current_best is None or revenue.revenue_usd_per_ha > current_best.revenue_usd_per_ha
        )
        if is_better:
            best[revenue.year] = revenue

    return {year: revenue.crop for year, revenue in best.items()}
