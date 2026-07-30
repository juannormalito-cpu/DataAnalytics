from src.application.use_cases.ingest_series import CommodityPriceTransformer


def test_converts_us_cents_per_bushel_to_usd_per_tonne():
    # Soja a 1000 US Cent/bushel = 10 USD/bushel; 1 bushel de soja = 27.2155 kg.
    transformer = CommodityPriceTransformer(
        variable_code="precio_soja_usd_ton", symbol="SOYBEAN-FUT",
        quote_divisor=100, kg_per_bushel=27.2155,
    )
    data = {"2024-01-02": {"SOYBEAN-FUT": {"close": 1000.0}}}

    observations = transformer.transform(data)

    assert len(observations) == 1
    expected = (1000.0 / 100) / 27.2155 * 1000
    assert round(observations[0].value, 2) == round(expected, 2)
    assert observations[0].province is None


def test_passes_through_prices_already_in_usd_per_tonne():
    transformer = CommodityPriceTransformer(
        variable_code="precio_urea_usd_ton", symbol="UREA", quote_divisor=1, kg_per_bushel=None
    )
    data = {"2024-01-02": {"UREA": {"close": 441.5}}}

    observations = transformer.transform(data)

    assert observations[0].value == 441.5


def test_skips_dates_without_the_requested_symbol():
    transformer = CommodityPriceTransformer(
        variable_code="precio_maiz_usd_ton", symbol="CORN", quote_divisor=100, kg_per_bushel=25.4012
    )
    data = {"2024-01-02": {"WHEAT": {"close": 500.0}}, "2024-01-03": {"CORN": {"close": None}}}

    assert transformer.transform(data) == []
