"""
This module contains unit tests for the OptionsFacade class.
"""

import pytest
from unittest.mock import patch
import pandas as pd
from backend.options_facade import OptionsFacade

# Mock data for testing
mock_expiration_dates = ["2024-06-07", "2024-07-07"]

mock_call_options = pd.DataFrame({
    "contractSymbol": ["AAPL240607C00100000", "AAPL240607C00110000", "AAPL240607C00120000"],
    "lastTradeDate": pd.to_datetime(["2024-06-07"] * 3),
    "strike": [100, 110, 120],
    "lastPrice": [10, 15, 20],
    "bid": [9, 14, 19],
    "ask": [11, 16, 21],
    "change": [0.5, 0.75, 1],
    "percentChange": [5, 7.5, 10],
    "volume": [100, 150, 200],
    "openInterest": [200, 250, 300],
    "impliedVolatility": [0.2, 0.25, 0.3]
})

mock_put_options = pd.DataFrame({
    "contractSymbol": ["AAPL240607P00100000", "AAPL240607P00105000", "AAPL240607P00110000"],
    "lastTradeDate": pd.to_datetime(["2024-06-07"] * 3),
    "strike": [100, 105, 110],
    "lastPrice": [10, 15, 20],
    "bid": [9, 14, 19],
    "ask": [11, 16, 21],
    "change": [0.5, 0.75, 1],
    "percentChange": [5, 7.5, 10],
    "volume": [100, 150, 200],
    "openInterest": [200, 250, 300],
    "impliedVolatility": [0.2, 0.25, 0.3]
})


@patch('backend.options_facade.yf.Ticker')
def test_get_expiration_dates(mock_ticker):
    """
    Test get_expiration_dates method of OptionsFacade class.
    :param mock_ticker: Mock of the Ticker class.
    :return: None
    """
    mock_ticker_instance = mock_ticker.return_value
    mock_ticker_instance.options = mock_expiration_dates

    options_facade = OptionsFacade("AAPL")
    expiration_dates = options_facade.get_expiration_dates()

    assert expiration_dates == mock_expiration_dates


@patch('backend.options_facade.yf.Ticker')
def test_get_options_data(mock_ticker):
    """
    Test get_options_data method of OptionsFacade class.
    :param mock_ticker: Mock of the Ticker class.
    :return: None
    """
    mock_ticker_instance = mock_ticker.return_value
    mock_ticker_instance.option_chain.return_value.calls = mock_call_options
    mock_ticker_instance.option_chain.return_value.puts = mock_put_options

    options_facade = OptionsFacade("AAPL")
    options_data = options_facade.get_options_data("2024-06-07")

    # Validate call options data
    call_options = options_data['calls']
    assert not call_options.empty
    assert list(call_options.columns) == ['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask',
                                          'change', 'percentChange', 'volume', 'openInterest', 'impliedVolatility']

    # Validate put options data
    put_options = options_data['puts']
    assert not put_options.empty
    assert list(put_options.columns) == ['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask',
                                         'change', 'percentChange', 'volume', 'openInterest', 'impliedVolatility']


if __name__ == "__main__":
    pytest.main()
