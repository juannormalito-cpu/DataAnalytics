"""
Motor financiero vertical-agnóstico: VAN, TIR, payback y índice de rentabilidad de un
proyecto, a partir de un flujo de fondos. Sirve igual para evaluar una campaña agrícola,
un ciclo de invernada o un turno forestal — lo único que cambia es cómo se arma el flujo
de fondos en cada vertical, no el motor.

Usa numpy-financial: numpy dejó de traer np.npv/np.irr hace años, así que el cálculo
financiero clásico (flujos de fondos) vive en este paquete aparte.
"""

from dataclasses import dataclass

import numpy_financial as npf


@dataclass(frozen=True)
class ProjectEvaluation:
    net_present_value: float
    internal_rate_of_return: float | None
    payback_period_years: float | None
    profitability_index: float | None


def net_present_value(cash_flows: list[float], discount_rate: float) -> float:
    """cash_flows[0] es la inversión inicial (típicamente negativa) en el año 0."""
    return float(npf.npv(discount_rate, cash_flows))


def internal_rate_of_return(cash_flows: list[float]) -> float | None:
    rate = npf.irr(cash_flows)
    if rate is None or rate != rate:  # NaN: no hay una TIR real (sin cambio de signo)
        return None
    return float(rate)


def payback_period(cash_flows: list[float]) -> float | None:
    """Años (fraccionarios) hasta recuperar la inversión inicial. None si nunca se recupera."""
    cumulative = cash_flows[0]
    if cumulative >= 0:
        return 0.0

    for year in range(1, len(cash_flows)):
        previous_cumulative = cumulative
        cumulative += cash_flows[year]
        if cumulative >= 0:
            return (year - 1) + (-previous_cumulative / cash_flows[year])

    return None


def profitability_index(cash_flows: list[float], discount_rate: float) -> float | None:
    """VAN de los flujos futuros sobre la inversión inicial. > 1 = proyecto rinde por encima
    de la tasa de descuento."""
    initial_investment = cash_flows[0]
    if initial_investment >= 0:
        return None

    npv = net_present_value(cash_flows, discount_rate)
    return npv / -initial_investment + 1


def evaluate_project(cash_flows: list[float], discount_rate: float) -> ProjectEvaluation:
    return ProjectEvaluation(
        net_present_value=net_present_value(cash_flows, discount_rate),
        internal_rate_of_return=internal_rate_of_return(cash_flows),
        payback_period_years=payback_period(cash_flows),
        profitability_index=profitability_index(cash_flows, discount_rate),
    )
