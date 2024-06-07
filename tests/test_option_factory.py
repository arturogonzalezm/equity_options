"""
This module contains tests for the OptionFactory class and its subclasses CallOption and PutOption.
"""

import pytest
from backend.option_factory import OptionFactory, CallOption, PutOption, Option

# Mock values for testing
stock_price = 100
strike_price = 100
time_to_expiry = 1  # 1 year
risk_free_rate = 0.05  # 5%
implied_volatility = 0.2  # 20%


# Test for OptionFactory
def test_create_call_option():
    """
    Test if the create_option method returns a CallOption object
    :param option_type: option type
    :return: None
    """
    option = OptionFactory.create_option("call", stock_price, strike_price, time_to_expiry, risk_free_rate,
                                         implied_volatility)
    assert isinstance(option, CallOption)


def test_create_put_option():
    """
    Test if the create_option method returns a PutOption object
    :param option_type: option type
    :return: None
    """
    option = OptionFactory.create_option("put", stock_price, strike_price, time_to_expiry, risk_free_rate,
                                         implied_volatility)
    assert isinstance(option, PutOption)


def test_create_invalid_option():
    """
    Test if the create_option method raises a ValueError for an invalid option type input
    ::param option_type: option type
    :return: None
    """
    with pytest.raises(ValueError):
        OptionFactory.create_option("invalid", stock_price, strike_price, time_to_expiry, risk_free_rate,
                                    implied_volatility)


# Test for CallOption
def test_call_option_calculate_price_and_greeks():
    """
    Test if the calculate_price_and_greeks method returns valid values
    :param stock_price: stock price
    :return: None
    """
    call_option = CallOption(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    call_price, delta, gamma, vega, theta, rho = call_option.calculate_price_and_greeks()
    assert call_price > 0
    assert -1 <= delta <= 1
    assert gamma > 0
    assert vega > 0
    assert theta < 0
    assert rho > 0


# Test for PutOption
def test_put_option_calculate_price_and_greeks():
    """
    Test if the calculate_price_and_greeks method returns valid values
    :param stock_price: stock price
    :return: None
    """
    put_option = PutOption(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    put_price, delta, gamma, vega, theta, rho = put_option.calculate_price_and_greeks()
    assert put_price > 0
    assert -1 <= delta <= 1
    assert gamma > 0
    assert vega > 0
    assert theta < 0
    assert rho < 0


if __name__ == "__main__":
    pytest.main()
