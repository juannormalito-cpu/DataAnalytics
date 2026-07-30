from src.domain.agriculture import margen_bruto_agricola
from src.domain.forestry import valor_masa_forestal
from src.domain.livestock import ganancia_por_cabeza


def test_margen_bruto_agricola():
    margen = margen_bruto_agricola(
        rendimiento_kg_ha=3500, precio_por_tonelada=280, costo_directo_por_ha=650
    )
    assert margen == 3500 / 1000 * 280 - 650


def test_ganancia_por_cabeza():
    ganancia = ganancia_por_cabeza(
        peso_inicial_kg=180,
        peso_final_kg=380,
        precio_compra_por_kilo=1.8,
        precio_venta_por_kilo=1.4,
        costo_engorde_total=120,
    )
    assert ganancia == (380 * 1.4) - (180 * 1.8) - 120


def test_valor_masa_forestal():
    valor = valor_masa_forestal(
        superficie_ha=50, volumen_m3_por_ha=220, precio_por_m3=18, costo_implantacion_por_ha=900
    )
    assert valor == (50 * 220 * 18) - (50 * 900)
