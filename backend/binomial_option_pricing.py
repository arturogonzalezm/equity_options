"""
This module contains the BinomialOptionPricing class which is used to calculate the price of a European call or put
"""

import numpy as np


class BinomialOptionPricing:
    """
    A class to calculate the price of a European call or put option using the binomial tree model.
    """
    def __init__(self, stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, steps, option_type):
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.time_to_expiry = time_to_expiry
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.steps = steps
        self.option_type = option_type

    def binomial_tree(self, stock_price=None, strike_price=None, time_to_expiry=None, risk_free_rate=None,
                      volatility=None, steps=None):
        """
        Calculate the price of a European call or put option using the binomial tree model.
        :param stock_price:
        :param strike_price:
        :param time_to_expiry:
        :param risk_free_rate:
        :param volatility:
        :param steps:
        :return:
        """
        stock_price = stock_price if stock_price is not None else self.stock_price
        strike_price = strike_price if strike_price is not None else self.strike_price
        time_to_expiry = time_to_expiry if time_to_expiry is not None else self.time_to_expiry
        risk_free_rate = risk_free_rate if risk_free_rate is not None else self.risk_free_rate
        volatility = volatility if volatility is not None else self.volatility
        steps = steps if steps is not None else self.steps

        dt = time_to_expiry / steps
        u = np.exp(volatility * np.sqrt(dt))
        d = 1 / u
        q = (np.exp(risk_free_rate * dt) - d) / (u - d)

        # Initialize asset prices at maturity
        asset_prices = np.zeros(steps + 1)
        for i in range(steps + 1):
            asset_prices[i] = stock_price * (u ** (steps - i)) * (d ** i)

        # Initialize option values at maturity
        option_values = np.zeros(steps + 1)
        for i in range(steps + 1):
            if self.option_type == "call":
                option_values[i] = max(0, asset_prices[i] - strike_price)
            else:  # put
                option_values[i] = max(0, strike_price - asset_prices[i])

        # Backward induction
        for step in range(steps - 1, -1, -1):
            for i in range(step + 1):
                option_values[i] = np.exp(-risk_free_rate * dt) * (
                            q * option_values[i] + (1 - q) * option_values[i + 1])
                asset_prices[i] = asset_prices[i] / u
                if self.option_type == "call":
                    option_values[i] = max(option_values[i], asset_prices[i] - strike_price)
                else:
                    option_values[i] = max(option_values[i], strike_price - asset_prices[i])

        return option_values[0]

    def calculate_greeks(self):
        """
        Calculate the Greeks (Delta, Gamma, Vega, Theta, Rho) of the option.
        :return: A tuple containing the Delta, Gamma, Vega, Theta, and Rho.
        """
        epsilon = 0.01

        # Calculate Delta
        option_price_up = self.binomial_tree(stock_price=self.stock_price + epsilon)
        option_price_down = self.binomial_tree(stock_price=self.stock_price - epsilon)
        delta = (option_price_up - option_price_down) / (2 * epsilon)

        # Calculate Gamma
        option_price_up2 = self.binomial_tree(stock_price=self.stock_price + 2 * epsilon)
        option_price_down2 = self.binomial_tree(stock_price=self.stock_price - 2 * epsilon)
        gamma = (option_price_up2 - 2 * option_price_up + option_price_down2) / (epsilon ** 2)

        # Calculate Theta
        option_price = self.binomial_tree()
        option_price_expired = self.binomial_tree(
            time_to_expiry=self.time_to_expiry - (self.time_to_expiry / self.steps))
        theta = (option_price_expired - option_price) / (self.time_to_expiry / self.steps)

        # Calculate Vega
        option_price_up_vol = self.binomial_tree(volatility=self.volatility + epsilon)
        option_price_down_vol = self.binomial_tree(volatility=self.volatility - epsilon)
        vega = (option_price_up_vol - option_price_down_vol) / (2 * epsilon)

        # Calculate Rho
        option_price_up_r = self.binomial_tree(risk_free_rate=self.risk_free_rate + epsilon)
        option_price_down_r = self.binomial_tree(risk_free_rate=self.risk_free_rate - epsilon)
        rho = (option_price_up_r - option_price_down_r) / (2 * epsilon)

        return delta, gamma, vega, theta, rho
