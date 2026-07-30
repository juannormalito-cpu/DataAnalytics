from src.domain.forecasting import project_linear_trend


def test_project_linear_trend_perfect_line():
    years = [2020, 2021, 2022, 2023]
    values = [100.0, 110.0, 120.0, 130.0]

    projection = project_linear_trend(years, values, years_ahead=2)

    assert [point.year for point in projection] == [2024, 2025]
    assert round(projection[0].value, 2) == 140.0
    assert round(projection[1].value, 2) == 150.0


def test_project_linear_trend_needs_at_least_two_points():
    assert project_linear_trend([2020], [100.0], years_ahead=3) == []
