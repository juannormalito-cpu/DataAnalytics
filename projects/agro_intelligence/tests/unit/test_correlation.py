from datetime import date

from src.application.use_cases.correlation import correlate, correlation_matrix
from src.domain.timeseries import Observation


def _obs(year: int, value: float) -> Observation:
    return Observation(variable_code="x", province=None, date=date(year, 1, 1), value=value)


def test_correlate_perfectly_correlated_series():
    series_a = [_obs(y, y) for y in range(2015, 2023)]
    series_b = [_obs(y, y * 2) for y in range(2015, 2023)]

    assert round(correlate(series_a, series_b), 4) == 1.0


def test_correlate_needs_at_least_three_overlapping_years():
    series_a = [_obs(2020, 1), _obs(2021, 2)]
    series_b = [_obs(2020, 1), _obs(2021, 2)]

    assert correlate(series_a, series_b) is None


def test_correlation_matrix_diagonal_is_one_and_symmetric():
    observations_by_label = {
        "A": [_obs(y, y) for y in range(2015, 2023)],
        "B": [_obs(y, y * 2) for y in range(2015, 2023)],
        "C": [_obs(y, -y) for y in range(2015, 2023)],
    }

    matrix = correlation_matrix(observations_by_label)

    assert round(matrix.loc["A", "A"], 4) == 1.0
    assert round(matrix.loc["A", "B"], 4) == 1.0
    assert round(matrix.loc["A", "C"], 4) == -1.0
    assert round(matrix.loc["A", "B"], 4) == round(matrix.loc["B", "A"], 4)
