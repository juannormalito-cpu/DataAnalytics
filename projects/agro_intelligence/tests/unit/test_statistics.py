from datetime import date

from src.application.use_cases.statistics import describe_stats
from src.domain.timeseries import Observation


def _obs(value: float, year: int = 2020) -> Observation:
    return Observation(variable_code="x", province=None, date=date(year, 1, 1), value=value)


def test_describe_stats_basic_metrics():
    observations = [_obs(v) for v in [10.0, 20.0, 30.0, 40.0, 50.0]]

    stats = describe_stats(observations)

    assert stats.count == 5
    assert stats.mean == 30.0
    assert stats.median == 30.0
    assert stats.minimum == 10.0
    assert stats.maximum == 50.0
    assert stats.coefficient_of_variation is not None
    assert round(stats.coefficient_of_variation, 2) == round((stats.std_dev / 30.0) * 100, 2)


def test_describe_stats_empty_returns_none():
    assert describe_stats([]) is None


def test_describe_stats_single_value_has_zero_std_dev():
    stats = describe_stats([_obs(42.0)])

    assert stats.std_dev == 0.0
    assert stats.coefficient_of_variation == 0.0
