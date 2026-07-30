"""Reglas de negocio de forestación."""


def valor_masa_forestal(
    superficie_ha: float,
    volumen_m3_por_ha: float,
    precio_por_m3: float,
    costo_implantacion_por_ha: float,
) -> float:
    """Valor de la masa forestal en pie a un turno dado, neto del costo de implantación."""
    ingreso_total = superficie_ha * volumen_m3_por_ha * precio_por_m3
    costo_total = superficie_ha * costo_implantacion_por_ha
    return ingreso_total - costo_total
