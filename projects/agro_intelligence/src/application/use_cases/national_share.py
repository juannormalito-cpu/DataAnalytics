"""Peso de una provincia en el total nacional: producción/existencia de la provincia
sobre el total del país (24 provincias), no solo relativa a nuestras 5 provincias
objetivo. Responde "qué peso tiene esta zona en el indicador macro real"."""

from dataclasses import dataclass

from src.domain.timeseries import Observation


@dataclass(frozen=True)
class ProvinceShare:
    province: str
    year: int
    share: float  # 0.0-1.0; ej. 0.18 = 18% del total nacional ese año


def compute_shares_by_province(
    provincial_observations: list[Observation], national_observations: list[Observation]
) -> list[ProvinceShare]:
    national_by_year = {
        observation.date.year: observation.value for observation in national_observations
    }

    shares = []
    for observation in provincial_observations:
        national_value = national_by_year.get(observation.date.year)
        if national_value:
            shares.append(
                ProvinceShare(
                    province=observation.province,
                    year=observation.date.year,
                    share=observation.value / national_value,
                )
            )
    return shares


def average_share_by_province(shares: list[ProvinceShare]) -> dict[str, float]:
    by_province: dict[str, list[float]] = {}
    for share in shares:
        by_province.setdefault(share.province, []).append(share.share)
    return {
        province: sum(values) / len(values) for province, values in by_province.items()
    }
