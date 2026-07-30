import pandas as pd

from src.application.use_cases.ingest_series import (
    AgricultureDepartmentTransformer,
    AgricultureNationalProductionTransformer,
    AgricultureProductionDepartmentTransformer,
    AgricultureProductionTransformer,
    AgricultureTransformer,
)


def _sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "cultivo": "soja total", "anio": 2020, "provincia": "Buenos Aires",
                "departamento": "Pergamino", "rendimiento_kgxha": 3000, "produccion_tm": 1000,
            },
            {
                "cultivo": "soja total", "anio": 2020, "provincia": "Buenos Aires",
                "departamento": "Junín", "rendimiento_kgxha": 3400, "produccion_tm": 1500,
            },
            {
                "cultivo": "trigo total", "anio": 2020, "provincia": "Buenos Aires",
                "departamento": "Pergamino", "rendimiento_kgxha": 2500, "produccion_tm": 800,
            },
            {
                "cultivo": "soja total", "anio": 2020, "provincia": "Chaco",
                "departamento": "Resistencia", "rendimiento_kgxha": 1800, "produccion_tm": 500,
            },
            {
                "cultivo": "algodón", "anio": 2020, "provincia": "Chaco",
                "departamento": "Resistencia", "rendimiento_kgxha": 800, "produccion_tm": 200,
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


def test_agriculture_production_transformer_sums_departments():
    observations = AgricultureProductionTransformer().transform(_sample_frame())

    soja = next(
        o
        for o in observations
        if o.variable_code == "produccion_soja_tm" and o.province == "Buenos Aires"
    )
    assert soja.value == 1000 + 1500  # suma, no promedio


def test_agriculture_production_department_transformer_keeps_departments_separate():
    observations = AgricultureProductionDepartmentTransformer().transform(_sample_frame())

    soja_observations = [o for o in observations if o.variable_code == "produccion_soja_tm_depto"]
    by_department = {o.province: o.value for o in soja_observations}

    assert by_department == {
        "Pergamino, Buenos Aires": 1000,
        "Junín, Buenos Aires": 1500,
    }


def test_agriculture_national_production_ignores_province_filter():
    observations = AgricultureNationalProductionTransformer().transform(_sample_frame())

    soja_nacional = next(
        o for o in observations if o.variable_code == "produccion_soja_tm_nacional"
    )
    assert soja_nacional.province is None
    # Buenos Aires (1000+1500) + Chaco (500), que quedaría afuera del filtro por provincia
    assert soja_nacional.value == 1000 + 1500 + 500
