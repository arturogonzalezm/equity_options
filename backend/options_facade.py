"""
This module is responsible for fetching options data from Yahoo Finance API.
"""
import yfinance as yf


class OptionsFacade:
    """
    A class to fetch options data for a given symbol.
    """
    def __init__(self, symbol):
        """
        Constructor for OptionsFacade class.
        :param symbol: The symbol for which options data is to be fetched.
        """
        self.ticker = yf.Ticker(symbol)

    @staticmethod
    def _extract_relevant_columns(options_df):
        """
        Extracts relevant columns from the options DataFrame.
        :param options_df: The options DataFrame.
        :return: DataFrame containing only the relevant columns.
        """
        relevant_columns = ['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change',
                            'percentChange', 'volume', 'openInterest', 'impliedVolatility']
        return options_df[relevant_columns]

    def get_options_data(self, expiration_date):
        """
        Fetches options data for a given expiration date.
        :param expiration_date: The expiration date for which options data is to be fetched.
        :return: A dictionary containing call and put options data.
        """
        options_chain = self.ticker.option_chain(expiration_date)
        call_options = self._extract_relevant_columns(options_chain.calls)
        put_options = self._extract_relevant_columns(options_chain.puts)

        return {
            'calls': call_options,
            'puts': put_options
        }

    def get_expiration_dates(self):
        """
        Fetches the expiration dates for the options.
        :return: A list of expiration dates.
        """
        return self.ticker.options
