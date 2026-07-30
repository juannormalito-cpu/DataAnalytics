import pandas as pd

from src.application.use_cases.ingest_series import (
    AgricultureDepartmentTransformer,
    AgricultureTransformer,
)


def _sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "cultivo": "soja total", "anio": 2020, "provincia": "Buenos Aires",
                "departamento": "Pergamino", "rendimiento_kgxha": 3000,
            },
            {
                "cultivo": "soja total", "anio": 2020, "provincia": "Buenos Aires",
                "departamento": "Junín", "rendimiento_kgxha": 3400,
            },
            {
                "cultivo": "trigo total", "anio": 2020, "provincia": "Buenos Aires",
                "departamento": "Pergamino", "rendimiento_kgxha": 2500,
            },
            {
                "cultivo": "algodón", "anio": 2020, "provincia": "Chaco",
                "departamento": "Resistencia", "rendimiento_kgxha": 800,
            },
        ]
    )


def test_agriculture_transformer_groups_by_province():
    observations = AgricultureTransformer().transform(_sample_frame())

    soja = next(o for o in observations if o.variable_code == "rendimiento_soja")
    assert soja.province == "Buenos Aires"
    assert soja.value == (3000 + 3400) / 2
    assert len(observations) == 2  # soja + trigo; algodón/Chaco quedan afuera


def test_agriculture_department_transformer_keeps_departments_separate():
    observations = AgricultureDepartmentTransformer().transform(_sample_frame())

    soja_observations = [o for o in observations if o.variable_code == "rendimiento_soja_depto"]
    provinces = {o.province for o in soja_observations}

    assert provinces == {"Pergamino, Buenos Aires", "Junín, Buenos Aires"}
