"""
This module contains the unit tests for the OptionPricing class.
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from backend.option_pricing import OptionPricing

# Mock values for testing
stock_symbol = "AAPL"
risk_free_rate = 0.01

mock_stock_data = {
    "Close": pd.Series([150, 152, 154, 156, 158], index=pd.date_range("2022-01-01", periods=5))
}

mock_call_options = pd.DataFrame({
    "contractSymbol": ["AAPL240607C00100000", "AAPL240607C00110000", "AAPL240607C00120000"],
    "strike": [100, 110, 120],
    "lastTradeDate": pd.to_datetime(["2024-06-07"] * 3),
    "impliedVolatility": [0.2, 0.25, 0.3],
    "volume": [100, 150, 200],
    "openInterest": [200, 250, 300],
    "lastPrice": [10, 15, 20],
    "bid": [9, 14, 19],
    "ask": [11, 16, 21],
    "change": [0.5, 0.75, 1],
    "percentChange": [5, 7.5, 10]
})

mock_put_options = pd.DataFrame({
    "contractSymbol": ["AAPL240607P00100000", "AAPL240607P00105000", "AAPL240607P00110000"],
    "strike": [100, 105, 110],
    "lastTradeDate": pd.to_datetime(["2024-06-07"] * 3),
    "impliedVolatility": [0.2, 0.25, 0.3],
    "volume": [100, 150, 200],
    "openInterest": [200, 250, 300],
    "lastPrice": [10, 15, 20],
    "bid": [9, 14, 19],
    "ask": [11, 16, 21],
    "change": [0.5, 0.75, 1],
    "percentChange": [5, 7.5, 10]
})


@patch('backend.option_pricing.yf.Ticker')
def test_retrieve_stock_data(mock_ticker):
    """
    Test the retrieve_stock_data method
    :param mock_ticker: mock Ticker class
    :return: None
    """
    mock_ticker_instance = mock_ticker.return_value
    mock_ticker_instance.history.return_value = mock_stock_data

    option_pricing = OptionPricing(stock_symbol, risk_free_rate)
    option_pricing.retrieve_stock_data()

    assert option_pricing.stock_price == 158


@patch('backend.option_pricing.yf.Ticker')
def test_retrieve_option_symbols(mock_ticker):
    """
    Test the retrieve_option_symbols method
    :param mock_ticker: mock Ticker class
    :return: None
    """
    mock_ticker_instance = mock_ticker.return_value
    mock_ticker_instance.options = ["2024-06-07"]
    mock_ticker_instance.option_chain.return_value.calls = mock_call_options
    mock_ticker_instance.option_chain.return_value.puts = mock_put_options

    option_pricing = OptionPricing(stock_symbol, risk_free_rate)
    option_pricing.retrieve_option_symbols()

    assert not option_pricing.call_options.empty
    assert not option_pricing.put_options.empty
    assert len(option_pricing.call_options) == 3
    assert len(option_pricing.put_options) == 3


@patch('backend.option_pricing.yf.Ticker')
def test_calculate_option_prices_and_greeks(mock_ticker):
    """
    Test the calculate_option_prices_and_greeks method
    :param mock_ticker: mock Ticker class
    :return: None
    """
    mock_ticker_instance = mock_ticker.return_value
    mock_ticker_instance.history.return_value = mock_stock_data
    mock_ticker_instance.options = ["2024-06-07"]
    mock_ticker_instance.option_chain.return_value.calls = mock_call_options
    mock_ticker_instance.option_chain.return_value.puts = mock_put_options

    option_pricing = OptionPricing(stock_symbol, risk_free_rate)
    option_pricing.retrieve_stock_data()
    option_pricing.retrieve_option_symbols()

    call_df, put_df = option_pricing.calculate_option_prices_and_greeks()

    assert not call_df.empty
    assert not put_df.empty

    for symbol in mock_call_options["contractSymbol"]:
        assert symbol in call_df["Option Symbol"].values

    for symbol in mock_put_options["contractSymbol"]:
        assert symbol in put_df["Option Symbol"].values


if __name__ == "__main__":
    pytest.main()
