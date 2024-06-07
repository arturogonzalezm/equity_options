"""
Test cases for PutOption class
"""

import pytest
from backend.put_option import PutOption

# Mock values for testing
stock_price = 100
strike_price = 100
time_to_expiry = 1  # 1 year
risk_free_rate = 0.05  # 5%
implied_volatility = 0.2  # 20%


# Test for PutOption with positive time to expiry
def test_put_option_calculate_price_and_greeks():
    """
    Test for PutOption with positive time to expiry
    :param stock_price: float: Stock price
    :return: None
    """
    put_option = PutOption(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    put_price, delta, gamma, vega, theta, rho = put_option.calculate_price_and_greeks()

    assert put_price > 0
    assert -1 <= delta <= 0
    assert gamma > 0
    assert vega > 0
    assert theta < 0
    assert rho < 0


# Test for PutOption with zero time to expiry
def test_put_option_zero_time_to_expiry():
    """
    Test for PutOption with zero time to expiry
    :param stock_price: float: Stock price
    :return: None
    """
    put_option = PutOption(stock_price, strike_price, 0, risk_free_rate, implied_volatility)
    put_price, delta, gamma, vega, theta, rho = put_option.calculate_price_and_greeks()

    assert put_price == max(strike_price - stock_price, 0)
    assert delta == 0
    assert gamma == 0
    assert vega == 0
    assert theta == 0
    assert rho == 0


# Test for PutOption with stock price greater than strike price
def test_put_option_out_of_the_money():
    """
    Test for PutOption with stock price greater than strike price
    :param stock_price: float: Stock price
    :return: None
    """
    put_option = PutOption(stock_price + 20, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    put_price, delta, gamma, vega, theta, rho = put_option.calculate_price_and_greeks()

    assert put_price > 0
    assert delta > -1 and delta < 0


# Test for PutOption with stock price less than strike price
def test_put_option_in_the_money():
    """
    Test for PutOption with stock price less than strike price
    :param stock_price: float: Stock price
    :return: None
    """
    put_option = PutOption(stock_price - 20, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    put_price, delta, gamma, vega, theta, rho = put_option.calculate_price_and_greeks()

    assert put_price > 0
    assert delta < -0.5


if __name__ == "__main__":
    pytest.main()
