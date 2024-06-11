"""
This is the main Streamlit app that will be run to launch the Option Pricing Calculator.
"""

import streamlit as st
from backend.options_facade import OptionsFacade

# Streamlit app title
st.title("Option Pricing Calculator")

# Input fields in the sidebar
st.sidebar.title("Input Parameters")
stock_symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")

# Create an OptionsFacade instance
options_facade = OptionsFacade(stock_symbol)

# Retrieve and display expiration dates
expiration_dates = options_facade.get_expiration_dates()
selected_expiration_date = st.sidebar.selectbox("Select Expiration Date", expiration_dates)

# Button to fetch options data
if st.sidebar.button("Retrieve Options Data"):
    try:
        options_data = options_facade.get_options_data(selected_expiration_date)

        st.subheader(f"Call Options for {stock_symbol} expiring on {selected_expiration_date}")
        st.dataframe(options_data['calls'])

        st.subheader(f"Put Options for {stock_symbol} expiring on {selected_expiration_date}")
        st.dataframe(options_data['puts'])

    except Exception as e:
        st.error(f"Error retrieving options data: {e}")

# Footer
st.write("Developed using Streamlit and the Black-Scholes Model")
