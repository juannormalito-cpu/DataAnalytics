"""Reglas de negocio de agricultura."""


def margen_bruto_agricola(
    rendimiento_kg_ha: float,
    precio_por_tonelada: float,
    costo_directo_por_ha: float,
) -> float:
    """Margen bruto en $/ha: ingreso por rendimiento menos costos directos (semilla,
    agroquímicos, labores)."""
    ingreso_por_ha = (rendimiento_kg_ha / 1000) * precio_por_tonelada
    return ingreso_por_ha - costo_directo_por_ha
