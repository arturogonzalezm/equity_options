"""
This script demonstrates how to use the OptionsFacade class to retrieve options data for a given symbol.
"""

from backend.options_facade import OptionsFacade
from backend.singleton_logger import logger


def main():
    """
    Main function to demonstrate the use of OptionsFacade class.
    :return: None
    """
    symbol = "AAPL"
    options_facade = OptionsFacade(symbol)

    expiration_dates = options_facade.get_expiration_dates()

    for expiration_date in expiration_dates:
        options_data = options_facade.get_options_data(expiration_date)

        logger.info(f"Call Options for {symbol} expiring on {expiration_date}:")
        logger.info(options_data['calls'])

        logger.info(f"\nPut Options for {symbol} expiring on {expiration_date}:")
        logger.info(options_data['puts'])


if __name__ == "__main__":
    main()
