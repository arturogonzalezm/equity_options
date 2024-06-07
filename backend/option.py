# backend/option.py
from abc import ABC, abstractmethod


class Option(ABC):
    def __init__(self, stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.time_to_expiry = time_to_expiry
        self.risk_free_rate = risk_free_rate
        self.implied_volatility = implied_volatility

    @abstractmethod
    def calculate_price_and_greeks(self):
        pass
