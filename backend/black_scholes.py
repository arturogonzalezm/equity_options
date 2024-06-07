# backend/black_scholes.py
import numpy as np
from scipy.stats import norm


def black_scholes_call(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility):
    if time_to_expiry <= 0:
        return max(stock_price - strike_price, 0), 0, 0, 0, 0, 0

    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * implied_volatility ** 2) * time_to_expiry) / (
            implied_volatility * np.sqrt(time_to_expiry))
    d2 = d1 - implied_volatility * np.sqrt(time_to_expiry)

    call_price = stock_price * norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (stock_price * implied_volatility * np.sqrt(time_to_expiry))
    vega = stock_price * norm.pdf(d1) * np.sqrt(time_to_expiry)
    theta = -(stock_price * norm.pdf(d1) * implied_volatility) / (
            2 * np.sqrt(time_to_expiry)) - risk_free_rate * strike_price * np.exp(
        -risk_free_rate * time_to_expiry) * norm.cdf(d2)
    rho = strike_price * time_to_expiry * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)

    return call_price, delta, gamma, vega, theta, rho


def black_scholes_put(stock_price, strike_price, time_to_expiry, risk_free_rate, implied_volatility):
    if time_to_expiry <= 0:
        return max(strike_price - stock_price, 0), 0, 0, 0, 0, 0

    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + 0.5 * implied_volatility ** 2) * time_to_expiry) / (
            implied_volatility * np.sqrt(time_to_expiry))
    d2 = d1 - implied_volatility * np.sqrt(time_to_expiry)

    put_price = strike_price * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)
    delta = norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (stock_price * implied_volatility * np.sqrt(time_to_expiry))
    vega = stock_price * norm.pdf(d1) * np.sqrt(time_to_expiry)
    theta = -(stock_price * norm.pdf(d1) * implied_volatility) / (
            2 * np.sqrt(time_to_expiry)) + risk_free_rate * strike_price * np.exp(
        -risk_free_rate * time_to_expiry) * norm.cdf(-d2)
    rho = -strike_price * time_to_expiry * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2)

    return put_price, delta, gamma, vega, theta, rho
