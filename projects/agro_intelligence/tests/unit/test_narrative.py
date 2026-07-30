from datetime import date

from src.application.use_cases.narrative import describe_series
from src.domain.timeseries import Observation


def test_describe_series_identifies_best_and_worst_year():
    observations = [
        Observation(variable_code="x", province=None, date=date(2020, 1, 1), value=100.0),
        Observation(variable_code="x", province=None, date=date(2021, 1, 1), value=50.0),
        Observation(variable_code="x", province=None, date=date(2022, 1, 1), value=200.0),
    ]

    text = describe_series(observations, label="Rendimiento soja", unit="kg/ha")

    assert "2022" in text
    assert "2021" in text
    assert "Rendimiento soja" in text


def test_describe_series_empty():
    assert "No hay datos" in describe_series([], label="X", unit="kg/ha")
