import pandas as pd

from src.application.use_cases.ingest_series import (
    LivestockStockDepartmentTransformer,
    LivestockStockNationalTransformer,
    LivestockStockTransformer,
)


def _sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "anio": 2019, "provincia": "Corrientes", "departamento": "Capital",
                "vacas": 1000, "vaquillonas": 200, "novillos": 100, "novillitos": 50,
                "terneros": 300, "terneras": 300, "toros": 20, "toritos": None, "bueyes": None,
            },
            {
                "anio": 2019, "provincia": "Corrientes", "departamento": "Goya",
                "vacas": 500, "vaquillonas": 100, "novillos": 50, "novillitos": 25,
                "terneros": 150, "terneras": 150, "toros": 10, "toritos": None, "bueyes": None,
            },
            {
                "anio": 2019, "provincia": "Chaco", "departamento": "Resistencia",
                "vacas": 2000, "vaquillonas": 400, "novillos": 200, "novillitos": 100,
                "terneros": 600, "terneras": 600, "toros": 40, "toritos": None, "bueyes": None,
            },
        ]
    )


def test_livestock_stock_transformer_sums_categories_and_departments():
    observations = LivestockStockTransformer().transform(_sample_frame())

    corrientes = next(o for o in observations if o.province == "Corrientes")
    assert corrientes.value == (1000 + 200 + 100 + 50 + 300 + 300 + 20) + (
        500 + 100 + 50 + 25 + 150 + 150 + 10
    )
    assert len(observations) == 1  # Chaco no está en las 5 provincias objetivo


def test_livestock_stock_department_transformer_keeps_departments_separate():
    observations = LivestockStockDepartmentTransformer().transform(_sample_frame())

    provinces = {o.province for o in observations}
    assert provinces == {"Capital, Corrientes", "Goya, Corrientes"}


def test_livestock_stock_national_transformer_includes_all_provinces():
    observations = LivestockStockNationalTransformer().transform(_sample_frame())

    assert len(observations) == 1
    assert observations[0].province is None
    corrientes_total = 1000 + 200 + 100 + 50 + 300 + 300 + 20 + 500 + 100 + 50 + 25 + 150 + 150 + 10
    chaco_total = 2000 + 400 + 200 + 100 + 600 + 600 + 40
    assert observations[0].value == corrientes_total + chaco_total
