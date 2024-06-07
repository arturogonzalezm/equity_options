# backend/option_pricing.py
import yfinance as yf
import pandas as pd
from backend.option_factory import OptionFactory
from backend.singleton_logger import logger


class OptionPricing:
    def __init__(self, stock_symbol, risk_free_rate):
        self.stock_symbol = stock_symbol
        self.risk_free_rate = risk_free_rate
        self.stock_price = None
        self.call_options = pd.DataFrame()
        self.put_options = pd.DataFrame()

    def retrieve_stock_data(self):
        try:
            stock = yf.Ticker(self.stock_symbol)
            history = stock.history(period="1y")
            self.stock_price = history["Close"].iloc[-1]
            logger.info(f"Retrieved stock data for {self.stock_symbol}")
        except Exception as e:
            logger.error(f"Error retrieving stock data: {e}")
            raise

    def retrieve_option_symbols(self):
        try:
            stock = yf.Ticker(self.stock_symbol)
            expiration_dates = stock.options
            if not expiration_dates:
                logger.warning(f"No expiration dates found for {self.stock_symbol}")
                return

            all_calls = []
            all_puts = []

            for date in expiration_dates:
                try:
                    option_chain = stock.option_chain(date)
                    all_calls.extend(option_chain.calls.to_dict('records'))
                    all_puts.extend(option_chain.puts.to_dict('records'))
                except Exception as e:
                    logger.error(f"Error retrieving options for expiration date {date}: {e}")
                    print(f"Error retrieving options for expiration date {date}: {e}")

            if all_calls:
                self.call_options = pd.DataFrame(all_calls)
            if all_puts:
                self.put_options = pd.DataFrame(all_puts)

            logger.info(f"Retrieved option symbols for {self.stock_symbol}")
        except Exception as e:
            logger.error(f"Error retrieving option symbols: {e}")
            raise

    def calculate_option_prices_and_greeks(self):
        call_results = []
        put_results = []

        for _, call_data in self.call_options.iterrows():
            try:
                call_strike_price = call_data["strike"]
                call_last_trade_date = pd.to_datetime(call_data["lastTradeDate"]).tz_localize(None)
                call_time_to_expiry = (call_last_trade_date - pd.Timestamp.now().tz_localize(None)).days / 365
                call_implied_volatility = call_data["impliedVolatility"]
                call_volume = call_data["volume"]
                call_open_interest = call_data["openInterest"]
                call_last_price = call_data["lastPrice"]
                call_bid = call_data["bid"]
                call_ask = call_data["ask"]
                call_change = call_data["change"]
                call_percent_change = call_data["percentChange"]

                call_option = OptionFactory.create_option("call", self.stock_price, call_strike_price,
                                                          call_time_to_expiry, self.risk_free_rate,
                                                          call_implied_volatility)
                call_price, call_delta, call_gamma, call_vega, call_theta, call_rho = call_option.calculate_price_and_greeks()

                call_results.append({
                    "Option Symbol": call_data["contractSymbol"],
                    "Last Trade Date": call_last_trade_date,
                    "Strike Price": call_strike_price,
                    "Time to Expiry (years)": call_time_to_expiry,
                    "Implied Volatility": call_implied_volatility,
                    "Volume": call_volume,
                    "Open Interest": call_open_interest,
                    "Last Price": call_last_price,
                    "Bid": call_bid,
                    "Ask": call_ask,
                    "Change": call_change,
                    "% Change": call_percent_change,
                    "Option Price": call_price,
                    "Delta": call_delta,
                    "Gamma": call_gamma,
                    "Vega": call_vega,
                    "Theta": call_theta,
                    "Rho": call_rho
                })
            except Exception as e:
                logger.error(f"Error calculating Greeks for call option {call_data['contractSymbol']}: {e}")

        for _, put_data in self.put_options.iterrows():
            try:
                put_strike_price = put_data["strike"]
                put_last_trade_date = pd.to_datetime(put_data["lastTradeDate"]).tz_localize(None)
                put_time_to_expiry = (put_last_trade_date - pd.Timestamp.now().tz_localize(None)).days / 365
                put_implied_volatility = put_data["impliedVolatility"]
                put_volume = put_data["volume"]
                put_open_interest = put_data["openInterest"]
                put_last_price = put_data["lastPrice"]
                put_bid = put_data["bid"]
                put_ask = put_data["ask"]
                put_change = put_data["change"]
                put_percent_change = put_data["percentChange"]

                put_option = OptionFactory.create_option("put", self.stock_price, put_strike_price,
                                                         put_time_to_expiry, self.risk_free_rate,
                                                         put_implied_volatility)
                put_price, put_delta, put_gamma, put_vega, put_theta, put_rho = put_option.calculate_price_and_greeks()

                put_results.append({
                    "Option Symbol": put_data["contractSymbol"],
                    "Last Trade Date": put_last_trade_date,
                    "Strike Price": put_strike_price,
                    "Time to Expiry (years)": put_time_to_expiry,
                    "Implied Volatility": put_implied_volatility,
                    "Volume": put_volume,
                    "Open Interest": put_open_interest,
                    "Last Price": put_last_price,
                    "Bid": put_bid,
                    "Ask": put_ask,
                    "Change": put_change,
                    "% Change": put_percent_change,
                    "Option Price": put_price,
                    "Delta": put_delta,
                    "Gamma": put_gamma,
                    "Vega": put_vega,
                    "Theta": put_theta,
                    "Rho": put_rho
                })
            except Exception as e:
                logger.error(f"Error calculating Greeks for put option {put_data['contractSymbol']}: {e}")

        return pd.DataFrame(call_results), pd.DataFrame(put_results)
