"""Reglas de negocio de ganadería."""


def ganancia_por_cabeza(
    peso_inicial_kg: float,
    peso_final_kg: float,
    precio_compra_por_kilo: float,
    precio_venta_por_kilo: float,
    costo_engorde_total: float,
) -> float:
    """Resultado de un ciclo de invernada/engorde por cabeza: venta menos compra y costos."""
    costo_compra = peso_inicial_kg * precio_compra_por_kilo
    ingreso_venta = peso_final_kg * precio_venta_por_kilo
    return ingreso_venta - costo_compra - costo_engorde_total
