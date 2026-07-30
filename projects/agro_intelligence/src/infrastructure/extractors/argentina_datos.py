"""
Cliente de api.argentinadatos.com — agrega series públicas argentinas (cotizaciones,
inflación, etc.) bajo un único endpoint REST simple, sin API key. Se usa acá para el
dólar blue, que no tiene una cotización "oficial" única (BCRA no lo publica).
"""

import requests
from shared_core.etl.contracts import Extractor

BASE_URL = "https://api.argentinadatos.com/v1/cotizaciones/dolares/blue"
TIMEOUT_SECONDS = 30


class DolarBlueExtractor(Extractor):
    def extract(self) -> list[dict]:
        response = requests.get(BASE_URL, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
