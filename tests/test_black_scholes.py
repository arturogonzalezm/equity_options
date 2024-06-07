"""
This module contains the tests for the black_scholes module.
"""

import pytest
from backend.black_scholes import black_scholes_call, black_scholes_put

# Mock values for testing
stock_price = 100
strike_price = 100
time_to_expiry = 1  # 1 year
risk_free_rate = 0.05  # 5%
implied_volatility = 0.2  # 20%


# Test for black_scholes_call with positive time to expiry
def test_black_scholes_call():
    """
    Test for black_scholes_call with positive time to expiry
    :param stock_price: float: Stock price
    :return: None
    """
    call_price, delta, gamma, vega, theta, rho = black_scholes_call(stock_price, strike_price, time_to_expiry,
                                                                    risk_free_rate, implied_volatility)

    assert call_price > 0
    assert 0 <= delta <= 1
    assert gamma > 0
    assert vega > 0
    assert theta < 0
    assert rho > 0


# Test for black_scholes_call with zero time to expiry
def test_black_scholes_call_zero_time_to_expiry():
    """
    Test for black_scholes_call with zero time to expiry
    :param stock_price: float: Stock price
    :return: None
    """
    call_price, delta, gamma, vega, theta, rho = black_scholes_call(stock_price, strike_price, 0, risk_free_rate,
                                                                    implied_volatility)

    assert call_price == max(stock_price - strike_price, 0)
    assert delta == 0
    assert gamma == 0
    assert vega == 0
    assert theta == 0
    assert rho == 0


# Test for black_scholes_put with positive time to expiry
def test_black_scholes_put():
    """
    Test for black_scholes_put with positive time to expiry
    :param stock_price: float: Stock price
    :return: None
    """
    put_price, delta, gamma, vega, theta, rho = black_scholes_put(stock_price, strike_price, time_to_expiry,
                                                                  risk_free_rate, implied_volatility)

    assert put_price > 0
    assert -1 <= delta <= 0
    assert gamma > 0
    assert vega > 0
    assert theta < 0
    assert rho < 0


# Test for black_scholes_put with zero time to expiry
def test_black_scholes_put_zero_time_to_expiry():
    """
    Test for black_scholes_put with zero time to expiry
    :param stock_price: float: Stock price
    :return: None
    """
    put_price, delta, gamma, vega, theta, rho = black_scholes_put(stock_price, strike_price, 0, risk_free_rate,
                                                                  implied_volatility)

    assert put_price == max(strike_price - stock_price, 0)
    assert delta == 0
    assert gamma == 0
    assert vega == 0
    assert theta == 0
    assert rho == 0


if __name__ == "__main__":
    pytest.main()
