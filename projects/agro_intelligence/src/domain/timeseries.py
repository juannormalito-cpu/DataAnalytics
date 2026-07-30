"""Modelo genérico de series históricas: soporta agricultura, ganadería, forestación y macro
con una única forma (Variable + Observation) en vez de una tabla distinta por fuente."""

from dataclasses import dataclass
from datetime import date

VERTICALS = ("agricultura", "ganaderia", "forestacion", "macro", "insumos")


@dataclass(frozen=True)
class Variable:
    code: str
    name: str
    unit: str
    vertical: str
    source: str


@dataclass(frozen=True)
class Observation:
    variable_code: str
    date: date
    value: float
    province: str | None = None
