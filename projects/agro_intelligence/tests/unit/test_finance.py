from src.domain.finance import (
    internal_rate_of_return,
    net_present_value,
    payback_period,
    profitability_index,
)


def test_net_present_value_known_case():
    # Ejemplo de manual: inversión de 1000, retornos de 300/300/300/300/300 al 10%.
    cash_flows = [-1000, 300, 300, 300, 300, 300]
    assert round(net_present_value(cash_flows, 0.10), 2) == 137.24


def test_internal_rate_of_return_known_case():
    cash_flows = [-1000, 300, 300, 300, 300, 300]
    irr = internal_rate_of_return(cash_flows)
    assert irr is not None
    assert round(irr, 4) == round(0.1523905269, 4)


def test_payback_period_recovers_partway_through_a_year():
    cash_flows = [-1000, 300, 400, 500, 600]
    assert round(payback_period(cash_flows), 2) == 2.6


def test_payback_period_never_recovers():
    cash_flows = [-1000, 100, 100]
    assert payback_period(cash_flows) is None


def test_profitability_index_above_one_means_value_creation():
    cash_flows = [-1000, 300, 300, 300, 300, 300]
    pi = profitability_index(cash_flows, 0.10)
    assert pi is not None
    assert pi > 1
