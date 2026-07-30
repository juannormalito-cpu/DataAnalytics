"""
Extractor genérico para los CSV públicos de datos.magyp.gob.ar / ambiente.gob.ar.

Implementa el contrato Extractor de shared_core.etl: extract() no transforma nada, solo
trae el dato crudo. Cómo mapear cada CSV a Observation vive en application/ (Transformer).

Nota real: el CSV de Estimaciones Agrícolas mezcla encodings de distintas décadas (1969-2024)
y algunas filas tienen caracteres corruptos (ver AgricultureTransformer). encoding="latin-1"
nunca falla al decodificar (mapea todo byte 0-255), a diferencia de utf-8/cp1252 estrictos.
"""

from io import StringIO

import pandas as pd
import requests
from shared_core.etl.contracts import Extractor

TIMEOUT_SECONDS = 30


class MagypCsvExtractor(Extractor):
    def __init__(self, url: str, delimiter: str = ",", encoding: str = "latin-1"):
        self.url = url
        self.delimiter = delimiter
        self.encoding = encoding

    def extract(self) -> pd.DataFrame:
        response = requests.get(self.url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        response.encoding = self.encoding
        return pd.read_csv(StringIO(response.text), delimiter=self.delimiter)
