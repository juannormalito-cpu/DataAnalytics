"""
Derechos de exportación (retenciones) por cultivo — la única carga impositiva agro que
es uniforme a nivel nacional y tiene una tasa pública, verificable y fechada. Ganancias,
Ingresos Brutos e Impuesto Inmobiliario Rural varían por provincia y situación fiscal de
cada empresa: NO se estiman acá, se marcan explícitamente como "consultar contador" en
vez de inventar una tasa que probablemente esté mal para el caso real de alguien.

Tasas vigentes según Decreto 423/2026 (verificado en fuentes de prensa citadas en el
README — las retenciones cambian con cada gestión, revisar antes de usar para decisiones
reales).
"""

from dataclasses import dataclass

EXPORT_DUTY_RATES = {
    "soja": 0.24,
    "maiz": 0.085,
    "trigo": 0.055,
}


@dataclass(frozen=True)
class TaxEstimate:
    crop: str
    gross_revenue_usd_per_ha: float
    export_duty_rate: float
    export_duty_usd_per_ha: float
    net_of_export_duty_usd_per_ha: float


def estimate_export_duty(crop: str, gross_revenue_usd_per_ha: float) -> TaxEstimate:
    rate = EXPORT_DUTY_RATES.get(crop)
    if rate is None:
        raise ValueError(f"Sin tasa de retención cargada para '{crop}'.")

    duty = gross_revenue_usd_per_ha * rate
    return TaxEstimate(
        crop=crop,
        gross_revenue_usd_per_ha=gross_revenue_usd_per_ha,
        export_duty_rate=rate,
        export_duty_usd_per_ha=duty,
        net_of_export_duty_usd_per_ha=gross_revenue_usd_per_ha - duty,
    )
