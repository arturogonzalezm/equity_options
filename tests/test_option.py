
"""
Test the Option abstract class and its subclasses CallOption and PutOption
"""
import pytest
from backend.option import Option
from backend.call_option import CallOption
from backend.put_option import PutOption


# Test the abstract class cannot be instantiated
def test_option_instantiation():
    """
    Test the abstract class cannot be instantiated
    :param stock_price: float: Stock price
    :return: None
    """
    with pytest.raises(TypeError):
        option = Option(100, 100, 1, 0.05, 0.2)


# Mock values for testing
stock_price = 100
strike_price = 100
time_to_expiry = 1  # 1 year
risk_free_rate = 0.05  # 5%
implied_volatility = 0.2  # 20%


# Test the CallOption subclass
def test_call_option_subclass():
    """
    Test the CallOption subclass
    :param stock_price: float: Stock price
    :return: None
    """
    call_option = CallOption(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    assert isinstance(call_option, Option)
    call_price, delta, gamma, vega, theta, rho = call_option.calculate_price_and_greeks()

    assert call_price > 0
    assert 0 <= delta <= 1
    assert gamma > 0
    assert vega > 0
    assert theta < 0
    assert rho > 0


# Test the PutOption subclass
def test_put_option_subclass():
    """
    Test the PutOption subclass
    :param stock_price: float: Stock price
    :return: None
    """
    put_option = PutOption(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
    assert isinstance(put_option, Option)
    put_price, delta, gamma, vega, theta, rho = put_option.calculate_price_and_greeks()

    assert put_price > 0
    assert -1 <= delta <= 0
    assert gamma > 0
    assert vega > 0
    assert theta < 0
    assert rho < 0


if __name__ == "__main__":
    pytest.main()
