"""
This module contains tests for the CallOption class.
"""
import pytest
from backend.call_option import CallOption

# Mock values for testing
stock_price = 100
strike_price = 100
time_to_expiry = 1  # 1 year
risk_free_rate = 0.05  # 5%
implied_volatility = 0.2  # 20%


# Test for CallOption with positive time to expiry
def test_call_option_calculate_price_and_greeks():
    """
    Test for CallOption with positive time to expiry
    :param stock_price:
    :return:
    """
    call_option = CallOption(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    call_price, delta, gamma, vega, theta, rho = call_option.calculate_price_and_greeks()

    assert call_price > 0
    assert 0 <= delta <= 1
    assert gamma > 0
    assert vega > 0
    assert theta < 0
    assert rho > 0


# Test for CallOption with zero time to expiry
def test_call_option_zero_time_to_expiry():
    """
    Test for CallOption with zero time to expiry
    :param stock_price:
    :return:
    """
    call_option = CallOption(stock_price, strike_price, 0, risk_free_rate, implied_volatility)
    call_price, delta, gamma, vega, theta, rho = call_option.calculate_price_and_greeks()

    assert call_price == max(stock_price - strike_price, 0)
    assert delta == 0
    assert gamma == 0
    assert vega == 0
    assert theta == 0
    assert rho == 0


# Test for CallOption with stock price greater than strike price
def test_call_option_in_the_money():
    """
    Test for CallOption with stock price greater than strike price
    :param stock_price:
    :return:
    """
    call_option = CallOption(stock_price + 20, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    call_price, delta, gamma, vega, theta, rho = call_option.calculate_price_and_greeks()

    assert call_price > 0
    assert delta > 0.5


# Test for CallOption with stock price less than strike price
def test_call_option_out_of_the_money():
    """
    Test for CallOption with stock price less than strike price
    :param stock_price:
    :return:
    """
    call_option = CallOption(stock_price - 20, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    call_price, delta, gamma, vega, theta, rho = call_option.calculate_price_and_greeks()

    assert call_price > 0
    assert delta < 0.5


if __name__ == "__main__":
    pytest.main()
