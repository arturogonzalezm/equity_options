"""
This module provides a facade for the yfinance library to retrieve options data for a given stock symbol.
"""

import yfinance as yf


class OptionsFacade:
    """
    Facade for yfinance library to retrieve options data for a given stock symbol.
    """
    def __init__(self, symbol):
        """
        Constructor for OptionsFacade
        :param symbol: Stock symbol
        """
        self.ticker = yf.Ticker(symbol)

    def get_options_data(self, expiration_date):
        """
        Retrieve options data for a given expiration date.
        :param expiration_date: Expiration date for options
        :return: Dictionary containing call and put options data
        """
        options_chain = self.ticker.option_chain(expiration_date)
        call_options = options_chain.calls
        put_options = options_chain.puts

        # Return relevant columns for call and put options
        return {
            'calls': call_options[
                ['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change', 'percentChange',
                 'volume', 'openInterest', 'impliedVolatility']],
            'puts': put_options[
                ['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change', 'percentChange',
                 'volume', 'openInterest', 'impliedVolatility']]
        }

    def get_expiration_dates(self):
        """
        Retrieve available expiration dates for options.
        :return: List of expiration dates
        """
        return self.ticker.options
