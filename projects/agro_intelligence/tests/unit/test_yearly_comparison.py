from datetime import date

from src.application.use_cases.yearly_comparison import (
    best_crop_by_revenue,
    best_crop_by_year,
    compute_gross_revenue,
    compute_relative_performance,
)
from src.domain.timeseries import Observation


def _obs(code: str, year: int, value: float) -> Observation:
    return Observation(variable_code=code, province=None, date=date(year, 1, 1), value=value)


def test_compute_relative_performance_normalizes_by_crop_average():
    observations_by_crop = {
        "soja": [
            _obs("rendimiento_soja", 2020, 2000.0),
            _obs("rendimiento_soja", 2021, 3000.0),
        ],
        "maiz": [
            _obs("rendimiento_maiz", 2020, 6000.0),
            _obs("rendimiento_maiz", 2021, 6000.0),
        ],
    }

    performances = compute_relative_performance(observations_by_crop)

    soja_2020 = next(p for p in performances if p.crop == "soja" and p.year == 2020)
    soja_2021 = next(p for p in performances if p.crop == "soja" and p.year == 2021)
    maiz_2020 = next(p for p in performances if p.crop == "maiz" and p.year == 2020)

    assert round(soja_2020.relative_performance, 2) == 0.8
    assert round(soja_2021.relative_performance, 2) == 1.2
    assert round(maiz_2020.relative_performance, 2) == 1.0


def test_best_crop_by_year_picks_highest_relative_performance():
    observations_by_crop = {
        "soja": [
            _obs("rendimiento_soja", 2020, 2000.0),
            _obs("rendimiento_soja", 2021, 1000.0),
        ],
        "maiz": [
            _obs("rendimiento_maiz", 2020, 6000.0),
            _obs("rendimiento_maiz", 2021, 9000.0),
        ],
    }

    performances = compute_relative_performance(observations_by_crop)
    best = best_crop_by_year(performances)

    assert best[2021] == "maiz"


def test_compute_gross_revenue_multiplies_yield_by_price():
    yields_by_crop = {
        "soja": [_obs("rendimiento_soja", 2020, 3000.0)],  # kg/ha
        "maiz": [_obs("rendimiento_maiz", 2020, 8000.0)],
    }
    prices_by_crop = {
        "soja": [_obs("precio_soja_usd_ton", 2020, 400.0)],  # USD/ton
        "maiz": [_obs("precio_maiz_usd_ton", 2020, 200.0)],
    }

    revenues = compute_gross_revenue(yields_by_crop, prices_by_crop)

    soja_revenue = next(r for r in revenues if r.crop == "soja")
    maiz_revenue = next(r for r in revenues if r.crop == "maiz")

    assert soja_revenue.revenue_usd_per_ha == (3000.0 / 1000) * 400.0
    assert maiz_revenue.revenue_usd_per_ha == (8000.0 / 1000) * 200.0
    assert best_crop_by_revenue(revenues)[2020] == "maiz"


def test_compute_gross_revenue_skips_years_without_price():
    yields_by_crop = {"soja": [_obs("rendimiento_soja", 1970, 1500.0)]}
    prices_by_crop = {"soja": [_obs("precio_soja_usd_ton", 2020, 400.0)]}

    assert compute_gross_revenue(yields_by_crop, prices_by_crop) == []


def test_compute_gross_revenue_skips_crops_without_price_data_at_all():
    yields_by_crop = {"trigo": [_obs("rendimiento_trigo", 2020, 3000.0)]}
    prices_by_crop = {}

    assert compute_gross_revenue(yields_by_crop, prices_by_crop) == []
