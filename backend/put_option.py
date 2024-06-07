# backend/put_option.py
from scipy.stats import norm
import numpy as np
from .option import Option


class PutOption(Option):
    def calculate_price_and_greeks(self):
        if self.time_to_expiry <= 0:
            return max(self.strike_price - self.stock_price, 0), 0, 0, 0, 0, 0

        d1 = (np.log(self.stock_price / self.strike_price) +
              (self.risk_free_rate + 0.5 * self.implied_volatility ** 2) * self.time_to_expiry) / (
                     self.implied_volatility * np.sqrt(self.time_to_expiry))
        d2 = d1 - self.implied_volatility * np.sqrt(self.time_to_expiry)

        put_price = self.strike_price * np.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(
            -d2) - self.stock_price * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (self.stock_price * self.implied_volatility * np.sqrt(self.time_to_expiry))
        vega = self.stock_price * norm.pdf(d1) * np.sqrt(self.time_to_expiry)
        theta = -(self.stock_price * norm.pdf(d1) * self.implied_volatility) / (
                2 * np.sqrt(self.time_to_expiry)) + self.risk_free_rate * self.strike_price * np.exp(
            -self.risk_free_rate * self.time_to_expiry) * norm.cdf(-d2)
        rho = -self.strike_price * self.time_to_expiry * np.exp(-self.risk_free_rate * self.time_to_expiry) * norm.cdf(
            -d2)

        return put_price, delta, gamma, vega, theta, rho
