"""Narrativa automática: convierte una serie de observaciones en un párrafo corto
(mejor año, peor año, promedio, tendencia) en vez de dejar que el usuario interprete
el gráfico solo. Texto generado por reglas simples sobre los datos, no por un LLM."""

from src.domain.timeseries import Observation


def describe_series(observations: list[Observation], label: str, unit: str) -> str:
    if not observations:
        return f"No hay datos de {label} para esta selección."

    yearly: dict[int, list[float]] = {}
    for observation in observations:
        yearly.setdefault(observation.date.year, []).append(observation.value)
    yearly_averages = {year: sum(values) / len(values) for year, values in yearly.items()}

    best_year = max(yearly_averages, key=yearly_averages.get)
    worst_year = min(yearly_averages, key=yearly_averages.get)
    average = sum(yearly_averages.values()) / len(yearly_averages)

    years_sorted = sorted(yearly_averages)
    first_half = years_sorted[: len(years_sorted) // 2] or years_sorted
    second_half = years_sorted[len(years_sorted) // 2 :]
    first_half_average = sum(yearly_averages[year] for year in first_half) / len(first_half)
    second_half_average = sum(yearly_averages[year] for year in second_half) / len(second_half)

    if second_half_average > first_half_average * 1.05:
        trend = "una tendencia creciente"
    elif second_half_average < first_half_average * 0.95:
        trend = "una tendencia decreciente"
    else:
        trend = "una tendencia relativamente estable"

    return (
        f"{label}: el mejor año fue {best_year} ({yearly_averages[best_year]:,.0f} {unit}) "
        f"y el más flojo {worst_year} ({yearly_averages[worst_year]:,.0f} {unit}). "
        f"Promedio del período: {average:,.0f} {unit}, con {trend} en la segunda mitad "
        f"de la serie respecto de la primera."
    )
