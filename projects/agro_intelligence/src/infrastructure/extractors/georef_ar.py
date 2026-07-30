"""
Cliente del Servicio de Normalización de Datos Geográficos de Argentina (georef-ar-api,
apis.datos.gob.ar/georef). Se usa para traer centroides de departamento — son datos
geográficos estáticos (no cambian), no series históricas, así que no pasan por el
pipeline de ingesta Extractor/Transformer/Loader: se consultan directamente y se
cachean en el dashboard.
"""

import requests

BASE_URL = "https://apis.datos.gob.ar/georef/api/departamentos"
TIMEOUT_SECONDS = 30


def fetch_department_centroids(province: str) -> dict[str, tuple[float, float]]:
    response = requests.get(
        BASE_URL,
        params={
            "provincia": province,
            "campos": "id,nombre,centroide",
            "max": 100,
            "formato": "json",
        },
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()

    return {
        departamento["nombre"]: (
            departamento["centroide"]["lat"],
            departamento["centroide"]["lon"],
        )
        for departamento in payload.get("departamentos", [])
    }
