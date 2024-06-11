"""
This module contains tests for the binomial option pricing model.
"""

import pytest
import numpy as np
from backend.binomial_option_pricing import BinomialOptionPricing


@pytest.fixture
def call_option():
    """
    Fixture to create a call option object.
    :return: BinomialOptionPricing object
    """
    return BinomialOptionPricing(
        stock_price=100,
        strike_price=100,
        time_to_expiry=1,
        risk_free_rate=0.05,
        volatility=0.2,
        steps=100,
        option_type="call"
    )


@pytest.fixture
def put_option():
    """
    Fixture to create a put option object.
    :return: BinomialOptionPricing object
    """
    return BinomialOptionPricing(
        stock_price=100,
        strike_price=100,
        time_to_expiry=1,
        risk_free_rate=0.05,
        volatility=0.2,
        steps=100,
        option_type="put"
    )


def test_binomial_tree_call(call_option):
    """
    Test the binomial tree method for a call option.
    :param call_option: Call option object
    :return: None
    """
    price = call_option.binomial_tree()
    assert price > 0, "Call option price should be greater than 0"


def test_binomial_tree_put(put_option):
    """
    Test the binomial tree method for a put option.
    :param put_option: Put option object
    :return: None
    """
    price = put_option.binomial_tree()
    assert price > 0, "Put option price should be greater than 0"


def test_calculate_greeks_call(call_option):
    """
    Test the calculation of Greeks for a call option.
    :param call_option: Call option object
    :return: None
    """
    delta, gamma, vega, theta, rho = call_option.calculate_greeks()
    assert np.isfinite(delta), "Delta should be a finite number"
    assert np.isfinite(gamma), "Gamma should be a finite number"
    assert np.isfinite(vega), "Vega should be a finite number"
    assert np.isfinite(theta), "Theta should be a finite number"
    assert np.isfinite(rho), "Rho should be a finite number"


def test_calculate_greeks_put(put_option):
    """
    Test the calculation of Greeks for a put option.
    :param put_option: Put option object
    :return: None
    """
    delta, gamma, vega, theta, rho = put_option.calculate_greeks()
    assert np.isfinite(delta), "Delta should be a finite number"
    assert np.isfinite(gamma), "Gamma should be a finite number"
    assert np.isfinite(vega), "Vega should be a finite number"
    assert np.isfinite(theta), "Theta should be a finite number"
    assert np.isfinite(rho), "Rho should be a finite number"
