"""
Cliente de CommodityPriceAPI (commoditypriceapi.com) para precios internacionales de
referencia de granos e insumos. Es un proxy: Argentina no publica un precio FAS/FOB en
serie abierta y descargable (solo PDFs, ver README) — el precio internacional convertido
a USD/tonelada es lo más cercano a un dato real y verificable que se pudo conseguir.

El endpoint /rates/time-series acepta como máximo 1 año por pedido, así que el extractor
pagina internamente por año calendario. La cuota del plan (2000 requests) se cuida
arrancando desde `start_year` en vez de traer todo el historial disponible (1990-).

El plan "lite" tiene distinta profundidad histórica según el símbolo (soja respondió
desde 2020, CORN recién desde 2023) — en vez de adivinar un año de arranque por símbolo,
se tolera el 404 "DATA_NOT_FOUND" de un año puntual y se sigue con el siguiente.
"""

import os
from datetime import date

import requests
from shared_core.etl.contracts import Extractor

BASE_URL = "https://api.commoditypriceapi.com/v2/rates/time-series"
TIMEOUT_SECONDS = 30


class CommodityPriceExtractor(Extractor):
    def __init__(self, symbol: str, start_year: int, end_year: int | None = None):
        self.symbol = symbol
        self.start_year = start_year
        self.end_year = end_year or date.today().year

    def extract(self) -> dict[str, dict]:
        api_key = os.environ.get("COMMODITY_API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "Falta COMMODITY_API_KEY. Agregala a projects/agro_intelligence/.env "
                "(ver .env.example)."
            )

        daily_rates: dict[str, dict] = {}
        for year in range(self.start_year, self.end_year + 1):
            response = requests.get(
                BASE_URL,
                params={
                    "symbols": self.symbol,
                    "startDate": f"{year}-01-01",
                    "endDate": f"{year}-12-31",
                },
                headers={"x-api-key": api_key},
                timeout=TIMEOUT_SECONDS,
            )
            if response.status_code == 404:
                body = response.json()
                if body.get("error") == "DATA_NOT_FOUND":
                    continue
            response.raise_for_status()

            payload = response.json()
            daily_rates.update(payload.get("rates", {}))

        return daily_rates
