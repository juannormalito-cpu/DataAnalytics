"""
Valores de referencia de arrendamiento y precio de tierra: NO son series históricas
ingeridas (no hay fuente estructurada y abierta, ver README), son valores puntuales de
prensa/informes especializados, citados y fechados. Se muestran como referencia gruesa,
no como dato oficial — la variación real depende de la zona exacta, calidad de suelo y
aptitud del campo, y para una decisión real hace falta una tasación profesional.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RentalReference:
    zone: str
    quintales_per_ha: float
    campaign: str
    source: str


@dataclass(frozen=True)
class LandPriceReference:
    province: str
    usd_per_ha_low: float
    usd_per_ha_high: float
    source: str


# Bolsa de Cereales de Córdoba, campaña 2025/26 (ver README para el link).
RENTAL_REFERENCES = [
    RentalReference("Marcos Juárez (Córdoba)", 17.5, "2025/26", "Bolsa de Cereales de Córdoba"),
    RentalReference("Unión (Córdoba)", 15.5, "2025/26", "Bolsa de Cereales de Córdoba"),
    RentalReference("Río Seco (Córdoba)", 8.0, "2025/26", "Bolsa de Cereales de Córdoba"),
    RentalReference("Promedio nacional", 11.5, "2025/26", "Bolsa de Cereales de Córdoba"),
]

# Rangos de prensa especializada (Agrofy News / Perfil), no un índice oficial.
LAND_PRICE_REFERENCES = {
    "Buenos Aires": LandPriceReference("Buenos Aires", 10_000, 35_000, "Agrofy News / Perfil"),
    "Santa Fe": LandPriceReference("Santa Fe", 4_000, 16_000, "Agrofy News / Perfil"),
    "Córdoba": LandPriceReference("Córdoba", 4_500, 8_000, "Agrofy News / Perfil (sur de Córdoba)"),
}


def rental_references_for(zone_hint: str) -> list[RentalReference]:
    return [r for r in RENTAL_REFERENCES if zone_hint.lower() in r.zone.lower()] or list(
        RENTAL_REFERENCES
    )


def land_price_reference_for(province: str) -> LandPriceReference | None:
    return LAND_PRICE_REFERENCES.get(province)
