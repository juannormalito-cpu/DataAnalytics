"""
Cliente de la API unificada de series de tiempo del Estado argentino
(https://apis.datos.gob.ar/series). Varios organismos (BCRA, INDEC, MAE/Rofex) publican
sus series ahí bajo un mismo endpoint REST, en vez de tener que scrapear cada sitio.

La API pagina de a MAX_ROWS_PER_REQUEST filas por pedido. Para el motor financiero importa
más la punta reciente de la serie (tasa de descuento actual) que el arranque histórico, así
que por default se pide en orden descendente (lo más nuevo primero).
"""

import requests
from shared_core.etl.contracts import Extractor

BASE_URL = "https://apis.datos.gob.ar/series/api/series/"
TIMEOUT_SECONDS = 30
MAX_ROWS_PER_REQUEST = 5000


class SeriesTiempoARExtractor(Extractor):
    def __init__(
        self,
        series_id: str,
        start_date: str | None = None,
        sort: str = "desc",
    ):
        self.series_id = series_id
        self.start_date = start_date
        self.sort = sort

    def extract(self) -> list[tuple[str, float]]:
        params: dict[str, str | int] = {
            "ids": self.series_id,
            "format": "json",
            "limit": MAX_ROWS_PER_REQUEST,
            "sort": self.sort,
        }
        if self.start_date:
            params["start_date"] = self.start_date

        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
        return [(row[0], row[1]) for row in payload["data"]]
