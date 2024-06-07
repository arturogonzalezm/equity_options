# backend/option_factory.py
from backend.black_scholes import black_scholes_call, black_scholes_put


class OptionFactory:
    @staticmethod
    def create_option(option_type, stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility):
        if option_type == "call":
            return CallOption(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
        elif option_type == "put":
            return PutOption(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility)
        else:
            raise ValueError("Invalid option type")


class Option:
    def __init__(self, stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.time_to_expiry = time_to_expiry
        self.risk_free_rate = risk_free_rate
        self.implied_volatility = implied_volatility

    def calculate_price_and_greeks(self):
        raise NotImplementedError("Must implement calculate_price_and_greeks method")


class CallOption(Option):
    def calculate_price_and_greeks(self):
        return black_scholes_call(self.stock_price, self.strike_price, self.time_to_expiry, self.risk_free_rate,
                                  self.implied_volatility)


class PutOption(Option):
    def calculate_price_and_greeks(self):
        return black_scholes_put(self.stock_price, self.strike_price, self.time_to_expiry, self.risk_free_rate,
                                 self.implied_volatility)
