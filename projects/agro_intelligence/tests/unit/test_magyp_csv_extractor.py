from unittest.mock import Mock, patch

from src.infrastructure.extractors.magyp_csv import MagypCsvExtractor


@patch("src.infrastructure.extractors.magyp_csv.requests.get")
def test_repeated_extract_reuses_cached_response(mock_get):
    response = Mock()
    response.text = "a,b\n1,2\n"
    response.raise_for_status.return_value = None
    mock_get.return_value = response

    first = MagypCsvExtractor("https://example.com/data.csv").extract()
    second = MagypCsvExtractor("https://example.com/data.csv").extract()

    assert mock_get.call_count == 1
    assert first.equals(second)


@patch("src.infrastructure.extractors.magyp_csv.requests.get")
def test_different_urls_are_not_shared(mock_get):
    response = Mock()
    response.text = "a,b\n1,2\n"
    response.raise_for_status.return_value = None
    mock_get.return_value = response

    MagypCsvExtractor("https://example.com/one.csv").extract()
    MagypCsvExtractor("https://example.com/two.csv").extract()

    assert mock_get.call_count == 2
