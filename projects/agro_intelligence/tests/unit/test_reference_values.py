from src.application.use_cases.reference_values import (
    land_price_reference_for,
    rental_references_for,
)


def test_rental_references_filters_by_zone_hint():
    results = rental_references_for("Córdoba")

    assert len(results) >= 3
    assert all("córdoba" in r.zone.lower() for r in results)


def test_rental_references_falls_back_to_all_when_no_match():
    results = rental_references_for("Zona Inexistente")

    assert len(results) == 4


def test_land_price_reference_for_known_province():
    reference = land_price_reference_for("Santa Fe")

    assert reference is not None
    assert reference.usd_per_ha_low < reference.usd_per_ha_high


def test_land_price_reference_for_unknown_province_is_none():
    assert land_price_reference_for("Corrientes") is None
