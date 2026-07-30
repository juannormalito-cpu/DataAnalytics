from datetime import date

from src.application.use_cases.national_share import (
    average_share_by_province,
    compute_shares_by_province,
)
from src.domain.timeseries import Observation


def _obs(province: str | None, year: int, value: float) -> Observation:
    return Observation(variable_code="x", province=province, date=date(year, 1, 1), value=value)


def test_compute_shares_by_province():
    provincial = [
        _obs("Buenos Aires", 2020, 30.0),
        _obs("Santa Fe", 2020, 20.0),
        _obs("Buenos Aires", 2021, 40.0),
    ]
    national = [_obs(None, 2020, 100.0), _obs(None, 2021, 100.0)]

    shares = compute_shares_by_province(provincial, national)

    ba_2020 = next(s for s in shares if s.province == "Buenos Aires" and s.year == 2020)
    santa_fe_2020 = next(s for s in shares if s.province == "Santa Fe" and s.year == 2020)

    assert ba_2020.share == 0.3
    assert santa_fe_2020.share == 0.2


def test_compute_shares_skips_years_without_national_total():
    provincial = [_obs("Buenos Aires", 1999, 30.0)]
    national = [_obs(None, 2020, 100.0)]

    assert compute_shares_by_province(provincial, national) == []


def test_average_share_by_province():
    shares = compute_shares_by_province(
        [_obs("Buenos Aires", 2020, 30.0), _obs("Buenos Aires", 2021, 50.0)],
        [_obs(None, 2020, 100.0), _obs(None, 2021, 100.0)],
    )

    averages = average_share_by_province(shares)

    assert averages["Buenos Aires"] == 0.4
