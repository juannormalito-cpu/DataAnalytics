"""
Ingesta de series históricas oficiales: agricultura, ganadería, forestación (proxy) y
macro (tipo de cambio oficial + dólar blue). Cablea Extractor -> Transformer -> Loader
(contratos de shared_core.etl) para cinco fuentes reales distintas sin duplicar la
lógica de guardado.
"""

from dataclasses import dataclass
from datetime import date

import pandas as pd
from shared_core.etl.contracts import Loader, Transformer

from src.domain.timeseries import Observation, Variable
from src.infrastructure.extractors.argentina_datos import DolarBlueExtractor
from src.infrastructure.extractors.commodity_price_api import CommodityPriceExtractor
from src.infrastructure.extractors.magyp_csv import MagypCsvExtractor
from src.infrastructure.extractors.series_tiempo_ar import SeriesTiempoARExtractor
from src.infrastructure.repositories.timeseries_repository import TimeSeriesRepository

AGRICULTURE_CSV_URL = (
    "https://datos.magyp.gob.ar/dataset/9e1e77ba-267e-4eaa-a59f-3296e86b5f36"
    "/resource/95d066e6-8a0f-4a80-b59d-6f28f88eacd5/download/estimaciones-agricolas-2026-03.csv"
)
LIVESTOCK_CSV_URL = (
    "https://datos.magyp.gob.ar/dataset/d769a8a5-af81-4192-a623-6e3844bf500e"
    "/resource/bd15f73c-fe07-41d9-9dd9-58e3244cad59/download/mercado-de-liniers-mensual-.csv"
)
LIVESTOCK_STOCK_CSV_URL = (
    "https://datos.magyp.gob.ar/dataset/c19a5875-fb39-48b6-b0b2-234382722afb"
    "/resource/1b920477-8112-4e12-bc2c-94b564f04183"
    "/download/existencias-bovinas-provincia-departamento-2008-2019.csv"
)
CATTLE_CATEGORY_COLUMNS = [
    "vacas",
    "vaquillonas",
    "novillos",
    "novillitos",
    "terneros",
    "terneras",
    "toros",
    "toritos",
    "bueyes",
]
FORESTRY_CSV_URL = "https://ciam.ambiente.gob.ar/dt_csv.php?dt_id=465"
FX_SERIES_ID = "168.1_T_CAMBI500_D_0_0_17"  # Tipo de Cambio A3500 (BCRA / MAE / Rofex)

# Buenos Aires y Corrientes no llevan tilde y salen limpios de la fuente; Córdoba y Entre
# Ríos sí, y algunas filas del CSV de estimaciones (1969-2024) tienen la tilde corrupta
# (bytes de reemplazo de un encoding perdido en el origen). Se matchea tolerando cualquier
# carácter en esa posición en vez de asumir un encoding "correcto" que la fuente no tiene.
PROVINCE_PATTERNS = {
    "Buenos Aires": r"^buenos aires$",
    "Santa Fe": r"^santa fe$",
    "Entre Ríos": r"^entre r.{1,3}os$",
    "Corrientes": r"^corrientes$",
    "Córdoba": r"^c.{1,3}rdoba$",
}
CROP_PATTERNS = {
    "soja": r"^soja total$",
    "maiz": r"^ma.{1,3}z$",  # la í de "maíz" aparece corrupta con 1 a 3 bytes según la fila
    "trigo": r"^trigo total$",
}

# CommodityPriceAPI: no hay precio FAS/FOB argentino en serie abierta (solo PDF, ver
# README) — se usa la cotización internacional de referencia (Chicago/CBOT) como proxy,
# convertida a USD/tonelada. "quote_divisor" es 100 cuando el precio viene en centavos de
# dólar (US Cent) y 1 cuando ya viene en USD. "kg_per_bushel" es None para lo que ya se
# cotiza por tonelada (urea).
#
# ZW-SPOT: el metadata de la API dice quote="USD", pero es falso — verificado contra el
# pico real de trigo de mayo 2022 (~11-12 USD/bushel): el valor crudo de la API en esas
# fechas es ~1100-1200, que solo tiene sentido como centavos, no dólares. Se trata igual
# que soja/maíz (divisor 100) en vez de confiar en el metadata de la fuente.
COMMODITY_CONFIG = {
    "soja": {"symbol": "SOYBEAN-FUT", "quote_divisor": 100, "kg_per_bushel": 27.2155},
    "maiz": {"symbol": "CORN", "quote_divisor": 100, "kg_per_bushel": 25.4012},
    "trigo": {"symbol": "ZW-SPOT", "quote_divisor": 100, "kg_per_bushel": 27.2155},
    "urea": {"symbol": "UREA", "quote_divisor": 1, "kg_per_bushel": None},
}
COMMODITY_START_YEAR = 2015  # cuida la cuota del plan free; se puede ampliar más adelante


def _filter_and_tag_agriculture(data: pd.DataFrame) -> pd.DataFrame:
    """Filtra el CSV de estimaciones agrícolas a los cultivos/provincias objetivo y les
    agrega columnas "crop"/"province" ya normalizadas. Lo comparten el transformer por
    provincia y el de por departamento, para no duplicar el matching tolerante a encoding."""
    province_mask = pd.Series(False, index=data.index)
    province_by_row = pd.Series(None, index=data.index, dtype=object)
    for province_name, pattern in PROVINCE_PATTERNS.items():
        matches = data["provincia"].str.match(pattern, case=False, na=False)
        province_mask |= matches
        province_by_row = province_by_row.mask(matches, province_name)

    crop_mask = pd.Series(False, index=data.index)
    crop_by_row = pd.Series(None, index=data.index, dtype=object)
    for crop_name, pattern in CROP_PATTERNS.items():
        matches = data["cultivo"].str.match(pattern, case=False, na=False)
        crop_mask |= matches
        crop_by_row = crop_by_row.mask(matches, crop_name)

    subset = data[province_mask & crop_mask].copy()
    subset["crop"] = crop_by_row[province_mask & crop_mask]
    subset["province"] = province_by_row[province_mask & crop_mask]
    return subset


class AgricultureTransformer(Transformer):
    """Estimaciones agrícolas MAGyP -> rendimiento (kg/ha) por cultivo/provincia/año, para
    soja/maíz/trigo en las 5 provincias objetivo."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        subset = _filter_and_tag_agriculture(data)
        grouped = subset.groupby(["crop", "province", "anio"], as_index=False)[
            "rendimiento_kgxha"
        ].mean()

        return [
            Observation(
                variable_code=f"rendimiento_{row.crop}",
                province=row.province,
                date=date(int(row.anio), 1, 1),
                value=float(row.rendimiento_kgxha),
            )
            for row in grouped.itertuples()
        ]


class AgricultureDepartmentTransformer(Transformer):
    """Mismo CSV, agrupado por departamento en vez de provincia — mayor zonificación para
    el mapa. Reusa Observation.province para guardar "Departamento, Provincia" (no es una
    provincia real, es la ubicación más granular que da la fuente)."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        subset = _filter_and_tag_agriculture(data)
        grouped = subset.groupby(["crop", "province", "departamento", "anio"], as_index=False)[
            "rendimiento_kgxha"
        ].mean()

        return [
            Observation(
                variable_code=f"rendimiento_{row.crop}_depto",
                province=f"{row.departamento}, {row.province}",
                date=date(int(row.anio), 1, 1),
                value=float(row.rendimiento_kgxha),
            )
            for row in grouped.itertuples()
        ]


class AgricultureProductionTransformer(Transformer):
    """Producción (toneladas) por cultivo/provincia/año. A diferencia del rendimiento
    (kg/ha, se promedia entre departamentos), la producción se SUMA: es una cantidad
    aditiva, no una tasa. Sirve como numerador para calcular el peso de cada provincia
    en la producción nacional."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        subset = _filter_and_tag_agriculture(data)
        grouped = subset.groupby(["crop", "province", "anio"], as_index=False)[
            "produccion_tm"
        ].sum()

        return [
            Observation(
                variable_code=f"produccion_{row.crop}_tm",
                province=row.province,
                date=date(int(row.anio), 1, 1),
                value=float(row.produccion_tm),
            )
            for row in grouped.itertuples()
        ]


class AgricultureProductionDepartmentTransformer(Transformer):
    """Producción (toneladas) por departamento — misma zonificación que rendimiento y
    existencia bovina, para que el mapa sea consistente entre variables."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        subset = _filter_and_tag_agriculture(data)
        grouped = subset.groupby(["crop", "province", "departamento", "anio"], as_index=False)[
            "produccion_tm"
        ].sum()

        return [
            Observation(
                variable_code=f"produccion_{row.crop}_tm_depto",
                province=f"{row.departamento}, {row.province}",
                date=date(int(row.anio), 1, 1),
                value=float(row.produccion_tm),
            )
            for row in grouped.itertuples()
        ]


class AgricultureNationalProductionTransformer(Transformer):
    """Mismo CSV, sin filtrar por provincia — total nacional (las 24 provincias) de
    producción por cultivo/año. Es el denominador para "qué peso tiene esta provincia
    en la producción nacional", no solo el peso relativo entre nuestras 5 provincias."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        crop_mask = pd.Series(False, index=data.index)
        crop_by_row = pd.Series(None, index=data.index, dtype=object)
        for crop_name, pattern in CROP_PATTERNS.items():
            matches = data["cultivo"].str.match(pattern, case=False, na=False)
            crop_mask |= matches
            crop_by_row = crop_by_row.mask(matches, crop_name)

        subset = data[crop_mask].copy()
        subset["crop"] = crop_by_row[crop_mask]
        grouped = subset.groupby(["crop", "anio"], as_index=False)["produccion_tm"].sum()

        return [
            Observation(
                variable_code=f"produccion_{row.crop}_tm_nacional",
                province=None,
                date=date(int(row.anio), 1, 1),
                value=float(row.produccion_tm),
            )
            for row in grouped.itertuples()
        ]


def _filter_and_tag_livestock(data: pd.DataFrame) -> pd.DataFrame:
    """Mismo matching tolerante a encoding que _filter_and_tag_agriculture — esta fuente
    (SENASA) tiene la misma corrupción de tildes en nombres de provincia."""
    province_mask = pd.Series(False, index=data.index)
    province_by_row = pd.Series(None, index=data.index, dtype=object)
    for province_name, pattern in PROVINCE_PATTERNS.items():
        matches = data["provincia"].str.match(pattern, case=False, na=False)
        province_mask |= matches
        province_by_row = province_by_row.mask(matches, province_name)

    subset = data[province_mask].copy()
    subset["province"] = province_by_row[province_mask]
    for column in CATTLE_CATEGORY_COLUMNS:
        subset[column] = pd.to_numeric(subset[column], errors="coerce").fillna(0)
    subset["total_cabezas"] = subset[CATTLE_CATEGORY_COLUMNS].sum(axis=1)
    return subset


class LivestockStockTransformer(Transformer):
    """SENASA — existencias bovinas -> cabezas totales por provincia/año (2008-2019).
    Suma las categorías (vacas, novillos, terneros, etc.) a un total de cabezas."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        subset = _filter_and_tag_livestock(data)
        grouped = subset.groupby(["province", "anio"], as_index=False)["total_cabezas"].sum()

        return [
            Observation(
                variable_code="existencia_bovina_cabezas",
                province=row.province,
                date=date(int(row.anio), 1, 1),
                value=float(row.total_cabezas),
            )
            for row in grouped.itertuples()
        ]


class LivestockStockDepartmentTransformer(Transformer):
    """Igual, agrupado por departamento — mayor zonificación para el mapa."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        subset = _filter_and_tag_livestock(data)
        grouped = subset.groupby(["province", "departamento", "anio"], as_index=False)[
            "total_cabezas"
        ].sum()

        return [
            Observation(
                variable_code="existencia_bovina_cabezas_depto",
                province=f"{row.departamento}, {row.province}",
                date=date(int(row.anio), 1, 1),
                value=float(row.total_cabezas),
            )
            for row in grouped.itertuples()
        ]


class LivestockStockNationalTransformer(Transformer):
    """Total nacional (todas las provincias, sin filtrar) de cabezas bovinas por año —
    denominador para el peso de cada provincia en el rodeo nacional."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        working = data.copy()
        for column in CATTLE_CATEGORY_COLUMNS:
            working[column] = pd.to_numeric(working[column], errors="coerce").fillna(0)
        working["total_cabezas"] = working[CATTLE_CATEGORY_COLUMNS].sum(axis=1)

        grouped = working.groupby("anio", as_index=False)["total_cabezas"].sum()

        return [
            Observation(
                variable_code="existencia_bovina_cabezas_nacional",
                province=None,
                date=date(int(row.anio), 1, 1),
                value=float(row.total_cabezas),
            )
            for row in grouped.itertuples()
        ]


class LivestockTransformer(Transformer):
    """Mercado de Liniers -> precio de novillo ($/kg vivo). Serie nacional: el mercado de
    referencia no publica desagregado por provincia."""

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        return [
            Observation(
                variable_code="precio_novillo_liniers",
                province=None,
                date=date(int(row["año"]), int(row["mes"]), 1),
                value=float(row["Precio - Novillos"]),
            )
            for _, row in data.iterrows()
        ]


class ForestryTransformer(Transformer):
    """
    Evolución de bosque nativo (MAyDS) -> variable de contexto forestal.

    Es la fuente pública más sólida encontrada, pero mide bosque NATIVO, no superficie
    IMPLANTADA (pino/eucalipto), que es lo que de verdad le importa a una forestal
    comercial en Corrientes/Entre Ríos. AFoA y la Dirección de Producción Forestal no
    publican un CSV abierto de plantaciones — queda pendiente como fuente a sumar más
    adelante. Mientras tanto sirve como variable de riesgo/presión de uso de suelo.
    """

    def transform(self, data: pd.DataFrame) -> list[Observation]:
        return [
            Observation(
                variable_code="bosque_nativo_ha",
                province=None,
                date=date(int(row["año"]), 1, 1),
                value=float(row["bosque_nativo_hectáreas"]),
            )
            for _, row in data.iterrows()
        ]


class FxTransformer(Transformer):
    """Serie de tiempo AR (tipo de cambio A3500) -> observación diaria macro."""

    def transform(self, data: list[tuple[str, float]]) -> list[Observation]:
        return [
            Observation(
                variable_code="tipo_cambio_a3500",
                province=None,
                date=date.fromisoformat(observation_date),
                value=float(value),
            )
            for observation_date, value in data
        ]


class BlueDollarTransformer(Transformer):
    """api.argentinadatos.com -> cotización de venta del dólar blue, diaria (2011-hoy)."""

    def transform(self, data: list[dict]) -> list[Observation]:
        return [
            Observation(
                variable_code="dolar_blue_venta",
                province=None,
                date=date.fromisoformat(row["fecha"]),
                value=float(row["venta"]),
            )
            for row in data
        ]


class CommodityPriceTransformer(Transformer):
    """CommodityPriceAPI (OHLC diario) -> precio de cierre en USD/tonelada."""

    def __init__(
        self, variable_code: str, symbol: str, quote_divisor: float, kg_per_bushel: float | None
    ):
        self.variable_code = variable_code
        self.symbol = symbol
        self.quote_divisor = quote_divisor
        self.kg_per_bushel = kg_per_bushel

    def transform(self, data: dict[str, dict]) -> list[Observation]:
        observations = []
        for date_str, symbols_on_date in data.items():
            entry = symbols_on_date.get(self.symbol)
            if not entry or entry.get("close") is None:
                continue

            price = entry["close"] / self.quote_divisor
            if self.kg_per_bushel is not None:
                price = price / self.kg_per_bushel * 1000  # USD/bushel -> USD/tonelada

            observations.append(
                Observation(
                    variable_code=self.variable_code,
                    province=None,
                    date=date.fromisoformat(date_str),
                    value=price,
                )
            )
        return observations


class ObservationLoader(Loader):
    def __init__(self, repository: TimeSeriesRepository):
        self.repository = repository

    def load(self, data: list[Observation]) -> None:
        self.repository.save_observations(data)


@dataclass(frozen=True)
class IngestionJob:
    name: str
    extractor: object
    transformer: Transformer
    variables: list[Variable]


def _commodity_jobs() -> list[IngestionJob]:
    jobs = []
    for crop, config in COMMODITY_CONFIG.items():
        variable_code = f"precio_{crop}_usd_ton"
        jobs.append(
            IngestionJob(
                name=f"precio_internacional_{crop}",
                extractor=CommodityPriceExtractor(
                    symbol=config["symbol"], start_year=COMMODITY_START_YEAR
                ),
                transformer=CommodityPriceTransformer(
                    variable_code=variable_code,
                    symbol=config["symbol"],
                    quote_divisor=config["quote_divisor"],
                    kg_per_bushel=config["kg_per_bushel"],
                ),
                variables=[
                    Variable(
                        code=variable_code,
                        name=f"Precio internacional {crop} (proxy CBOT, USD/ton)",
                        unit="USD/ton",
                        vertical="insumos" if crop == "urea" else "agricultura",
                        source=f"commoditypriceapi.com symbol={config['symbol']}",
                    )
                ],
            )
        )
    return jobs


def build_catalog() -> list[IngestionJob]:
    return [
        IngestionJob(
            name="agricultura_rendimientos",
            extractor=MagypCsvExtractor(AGRICULTURE_CSV_URL),
            transformer=AgricultureTransformer(),
            variables=[
                Variable(
                    code=f"rendimiento_{crop}",
                    name=f"Rendimiento {crop}",
                    unit="kg/ha",
                    vertical="agricultura",
                    source=AGRICULTURE_CSV_URL,
                )
                for crop in CROP_PATTERNS
            ],
        ),
        IngestionJob(
            name="agricultura_rendimientos_departamento",
            extractor=MagypCsvExtractor(AGRICULTURE_CSV_URL),
            transformer=AgricultureDepartmentTransformer(),
            variables=[
                Variable(
                    code=f"rendimiento_{crop}_depto",
                    name=f"Rendimiento {crop} por departamento",
                    unit="kg/ha",
                    vertical="agricultura",
                    source=AGRICULTURE_CSV_URL,
                )
                for crop in CROP_PATTERNS
            ],
        ),
        IngestionJob(
            name="agricultura_produccion",
            extractor=MagypCsvExtractor(AGRICULTURE_CSV_URL),
            transformer=AgricultureProductionTransformer(),
            variables=[
                Variable(
                    code=f"produccion_{crop}_tm",
                    name=f"Producción {crop} (toneladas)",
                    unit="tn",
                    vertical="agricultura",
                    source=AGRICULTURE_CSV_URL,
                )
                for crop in CROP_PATTERNS
            ],
        ),
        IngestionJob(
            name="agricultura_produccion_departamento",
            extractor=MagypCsvExtractor(AGRICULTURE_CSV_URL),
            transformer=AgricultureProductionDepartmentTransformer(),
            variables=[
                Variable(
                    code=f"produccion_{crop}_tm_depto",
                    name=f"Producción {crop} por departamento (toneladas)",
                    unit="tn",
                    vertical="agricultura",
                    source=AGRICULTURE_CSV_URL,
                )
                for crop in CROP_PATTERNS
            ],
        ),
        IngestionJob(
            name="agricultura_produccion_nacional",
            extractor=MagypCsvExtractor(AGRICULTURE_CSV_URL),
            transformer=AgricultureNationalProductionTransformer(),
            variables=[
                Variable(
                    code=f"produccion_{crop}_tm_nacional",
                    name=f"Producción nacional {crop} (toneladas, 24 provincias)",
                    unit="tn",
                    vertical="agricultura",
                    source=AGRICULTURE_CSV_URL,
                )
                for crop in CROP_PATTERNS
            ],
        ),
        IngestionJob(
            name="ganaderia_existencias",
            extractor=MagypCsvExtractor(LIVESTOCK_STOCK_CSV_URL),
            transformer=LivestockStockTransformer(),
            variables=[
                Variable(
                    code="existencia_bovina_cabezas",
                    name="Existencia bovina (cabezas)",
                    unit="cabezas",
                    vertical="ganaderia",
                    source=LIVESTOCK_STOCK_CSV_URL,
                )
            ],
        ),
        IngestionJob(
            name="ganaderia_existencias_departamento",
            extractor=MagypCsvExtractor(LIVESTOCK_STOCK_CSV_URL),
            transformer=LivestockStockDepartmentTransformer(),
            variables=[
                Variable(
                    code="existencia_bovina_cabezas_depto",
                    name="Existencia bovina por departamento (cabezas)",
                    unit="cabezas",
                    vertical="ganaderia",
                    source=LIVESTOCK_STOCK_CSV_URL,
                )
            ],
        ),
        IngestionJob(
            name="ganaderia_existencias_nacional",
            extractor=MagypCsvExtractor(LIVESTOCK_STOCK_CSV_URL),
            transformer=LivestockStockNationalTransformer(),
            variables=[
                Variable(
                    code="existencia_bovina_cabezas_nacional",
                    name="Existencia bovina nacional (cabezas, 24 provincias)",
                    unit="cabezas",
                    vertical="ganaderia",
                    source=LIVESTOCK_STOCK_CSV_URL,
                )
            ],
        ),
        IngestionJob(
            name="ganaderia_precio_novillo",
            extractor=MagypCsvExtractor(LIVESTOCK_CSV_URL, encoding="utf-8-sig"),
            transformer=LivestockTransformer(),
            variables=[
                Variable(
                    code="precio_novillo_liniers",
                    name="Precio novillo (Mercado de Liniers)",
                    unit="$/kg vivo",
                    vertical="ganaderia",
                    source=LIVESTOCK_CSV_URL,
                )
            ],
        ),
        IngestionJob(
            name="forestacion_bosque_nativo",
            extractor=MagypCsvExtractor(FORESTRY_CSV_URL, delimiter=";", encoding="utf-8-sig"),
            transformer=ForestryTransformer(),
            variables=[
                Variable(
                    code="bosque_nativo_ha",
                    name="Superficie de bosque nativo (proxy forestal)",
                    unit="ha",
                    vertical="forestacion",
                    source=FORESTRY_CSV_URL,
                )
            ],
        ),
        IngestionJob(
            name="macro_tipo_cambio",
            extractor=SeriesTiempoARExtractor(FX_SERIES_ID),
            transformer=FxTransformer(),
            variables=[
                Variable(
                    code="tipo_cambio_a3500",
                    name="Tipo de cambio oficial mayorista (A3500)",
                    unit="$/USD",
                    vertical="macro",
                    source=f"apis.datos.gob.ar/series id={FX_SERIES_ID}",
                )
            ],
        ),
        IngestionJob(
            name="macro_dolar_blue",
            extractor=DolarBlueExtractor(),
            transformer=BlueDollarTransformer(),
            variables=[
                Variable(
                    code="dolar_blue_venta",
                    name="Dólar blue (venta)",
                    unit="$/USD",
                    vertical="macro",
                    source="api.argentinadatos.com/v1/cotizaciones/dolares/blue",
                )
            ],
        ),
        *_commodity_jobs(),
    ]


def run_ingestion(repository: TimeSeriesRepository) -> dict[str, int]:
    loader = ObservationLoader(repository)
    results: dict[str, int] = {}

    for job in build_catalog():
        for variable in job.variables:
            repository.upsert_variable(variable)

        raw = job.extractor.extract()
        observations = job.transformer.transform(raw)
        loader.load(observations)
        results[job.name] = len(observations)

    return results
