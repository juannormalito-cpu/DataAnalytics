import pytest

from src.domain.taxation import estimate_export_duty


def test_estimate_export_duty_soja():
    result = estimate_export_duty("soja", gross_revenue_usd_per_ha=1000.0)

    assert result.export_duty_rate == 0.24
    assert result.export_duty_usd_per_ha == 240.0
    assert result.net_of_export_duty_usd_per_ha == 760.0


def test_estimate_export_duty_unknown_crop_raises():
    with pytest.raises(ValueError):
        estimate_export_duty("girasol", gross_revenue_usd_per_ha=1000.0)
