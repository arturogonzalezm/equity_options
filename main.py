"""
This script is the entry point for the application. It retrieves stock data and calculates option prices and Greeks.
"""
from backend.config import stock_symbol, call_symbols, put_symbols, risk_free_rate
from backend.option_pricing import OptionPricing
from backend.singleton_logger import logger


def main():
    option_pricing = OptionPricing(stock_symbol, call_symbols, put_symbols, risk_free_rate)
    option_pricing.retrieve_stock_data()

    try:
        call_df, put_df = option_pricing.calculate_option_prices_and_greeks()
        logger.info("Call Options:")
        logger.info("\n" + call_df.to_string())
        logger.info("Put Options:")
        logger.info("\n" + put_df.to_string())
    except Exception as e:
        logger.error(f"Error calculating option prices and Greeks: {e}")


if __name__ == "__main__":
    main()
