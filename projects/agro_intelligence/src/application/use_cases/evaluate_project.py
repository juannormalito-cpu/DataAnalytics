"""Caso de uso: evaluar un proyecto productivo (agrícola, ganadero o forestal) dado su
flujo de fondos. Vertical-agnóstico — la vertical solo importa a la hora de armar el
flujo de fondos, no en la evaluación en sí."""

from src.domain.finance import ProjectEvaluation, evaluate_project


def evaluate(cash_flows: list[float], discount_rate: float) -> ProjectEvaluation:
    return evaluate_project(cash_flows, discount_rate)
