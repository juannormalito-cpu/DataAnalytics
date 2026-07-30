from unittest.mock import Mock, patch

from src.infrastructure.extractors.commodity_price_api import CommodityPriceExtractor


def _response(status_code: int, payload: dict) -> Mock:
    response = Mock()
    response.status_code = status_code
    response.json.return_value = payload
    if status_code == 404:
        response.raise_for_status.side_effect = Exception("should not be called on skip")
    else:
        response.raise_for_status.return_value = None
    return response


@patch.dict("os.environ", {"COMMODITY_API_KEY": "fake-key"})
@patch("src.infrastructure.extractors.commodity_price_api.requests.get")
def test_skips_years_with_no_data_and_keeps_going(mock_get):
    not_found = _response(404, {"error": "DATA_NOT_FOUND"})
    found = _response(
        200, {"rates": {"2024-01-02": {"CORN": {"close": 470.0}}}}
    )
    mock_get.side_effect = [not_found, found]

    extractor = CommodityPriceExtractor(symbol="CORN", start_year=2023, end_year=2024)
    result = extractor.extract()

    assert result == {"2024-01-02": {"CORN": {"close": 470.0}}}
    assert mock_get.call_count == 2
