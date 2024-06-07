import streamlit as st
import pandas as pd
import yfinance as yf
from backend.config import risk_free_rate
from backend.option_pricing import OptionPricing
from backend.singleton_logger import logger

# Streamlit app title
st.title("Option Pricing Calculator")

# Input fields in the sidebar
st.sidebar.title("Input Parameters")
stock_symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")


def color_negative_red_positive_green(val):
    """
    Apply red color to negative numbers and green color to positive numbers
    :param val:
    :return: CSS style
    """
    try:
        val = float(val)
        if val < 0:
            color = 'red'
        elif val == 0:
            color = 'black'
        else:
            color = 'green'
        return f'color: {color}'
    except ValueError:
        return ''  # If not a number, do not apply any color


def apply_color(df):
    styles = pd.DataFrame('', index=df.index, columns=df.columns)
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        styles[col] = df[col].map(color_negative_red_positive_green)
    return styles


# Retrieve stock information and calculate option prices when the button is pressed
if st.sidebar.button("Retrieve and Calculate"):
    try:
        stock = yf.Ticker(stock_symbol)
        stock_info = stock.info
        company_name = stock_info.get('longName', 'N/A')

        st.markdown(f"### {company_name} ({stock_symbol})")

        option_pricing = OptionPricing(stock_symbol, risk_free_rate)
        option_pricing.retrieve_stock_data()
        option_pricing.retrieve_option_symbols()

        if not option_pricing.call_options.empty or not option_pricing.put_options.empty:
            call_df, put_df = option_pricing.calculate_option_prices_and_greeks()

            if not call_df.empty:
                st.subheader("Call Option Prices and Greeks")
                styled_call_df = call_df.style.apply(apply_color, axis=None)
                st.dataframe(styled_call_df)

            if not put_df.empty:
                st.subheader("Put Option Prices and Greeks")
                styled_put_df = put_df.style.apply(apply_color, axis=None)
                st.dataframe(styled_put_df)
        else:
            st.warning("No options found for the given stock symbol.")

    except Exception as e:
        st.error(f"Error retrieving and calculating option symbols: {e}")
        logger.error(f"Error retrieving and calculating option symbols: {e}")

# Footer
st.write("Developed using Streamlit and the Black-Scholes Model")
