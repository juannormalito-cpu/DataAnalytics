"""
Extractor genérico para los CSV públicos de datos.magyp.gob.ar / ambiente.gob.ar.

Implementa el contrato Extractor de shared_core.etl: extract() no transforma nada, solo
trae el dato crudo. Cómo mapear cada CSV a Observation vive en application/ (Transformer).

Nota real: el CSV de Estimaciones Agrícolas mezcla encodings de distintas décadas (1969-2024)
y algunas filas tienen caracteres corruptos (ver AgricultureTransformer). encoding="latin-1"
nunca falla al decodificar (mapea todo byte 0-255), a diferencia de utf-8/cp1252 estrictos.

Varias IngestionJob comparten la misma URL (ej. el CSV de estimaciones agrícolas alimenta
rendimiento por provincia, por departamento, producción y producción nacional) — sin
cachear, una sola corrida de `ingest` pedía el mismo archivo 3-4 veces seguidas y la fuente
empezaba a devolver 429 (Too Many Requests). El caché es por proceso (vive mientras dura
el `python main.py ingest`), no persiste entre corridas.
"""

from io import StringIO

import pandas as pd
import requests
from shared_core.etl.contracts import Extractor

TIMEOUT_SECONDS = 30

_csv_cache: dict[tuple[str, str, str], pd.DataFrame] = {}


class MagypCsvExtractor(Extractor):
    def __init__(self, url: str, delimiter: str = ",", encoding: str = "latin-1"):
        self.url = url
        self.delimiter = delimiter
        self.encoding = encoding

    def extract(self) -> pd.DataFrame:
        cache_key = (self.url, self.delimiter, self.encoding)
        cached = _csv_cache.get(cache_key)
        if cached is not None:
            return cached.copy()

        response = requests.get(self.url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        response.encoding = self.encoding
        frame = pd.read_csv(StringIO(response.text), delimiter=self.delimiter)

        _csv_cache[cache_key] = frame
        return frame.copy()
