# Option Pricing Calculator

This project provides an implementation of an option pricing calculator using the Black-Scholes model. It includes classes for call and put options, an abstract `Option` class, and functionality to retrieve stock and option data from Yahoo Finance. The project also includes unit tests using `pytest`.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/arturogonzalezm/equity_options.git
   cd equity_options
    ```
   
2. Install the required packages:

    ```sh
    python.exe -m pip install --upgrade pip
    python.exe -m pip install -r .\requirements.txt
    ```
   
3. Project Structure:

    ```sh
    equity_options/
               │
               ├── backend/
               │   ├── __init__.py
               │   ├── black_scholes.py
               │   ├── call_option.py
               │   ├── put_option.py
               │   ├── option.py
               │   ├── option_pricing.py
               │   ├── option_factory.py
               │   └── singleton_logger.py
               │
               ├── tests/
               │   ├── __init__.py
               │   ├── test_black_scholes.py
               │   ├── test_call_option.py
               │   ├── test_put_option.py
               │   ├── test_option.py
               │   ├── test_option_pricing.py
               │   └── test_singleton_logger.py
               │
               ├── app.py
               ├── requirements.txt
               └── README.md
    ```

## Class Diagram

```mermaid
classDiagram
    class Option {
        <<abstract>>
        - stock_price: float
        - strike_price: float
        - time_to_expiry: float
        - risk_free_rate: float
        - implied_volatility: float
        + calculate_price_and_greeks()*
    }

    Option <|-- CallOption
    Option <|-- PutOption
    OptionFactory --> CallOption
    OptionFactory --> PutOption

    class CallOption {
        + calculate_price_and_greeks()
    }

    class PutOption {
        + calculate_price_and_greeks()
    }

    class OptionFactory {
        + create_option(option_type: str, stock_price: float, strike_price: float, time_to_expiry: float, risk_free_rate: float, implied_volatility: float) Option
    }

    class OptionPricing {
        - stock_symbol: str
        - risk_free_rate: float
        - stock_price: float
        - call_options: DataFrame
        - put_options: DataFrame
        + retrieve_stock_data()
        + retrieve_option_symbols()
        + calculate_option_prices_and_greeks()
    }

    class SingletonLogger {
        - _instance: SingletonLogger
        - _lock: RLock
        + get_logger() Logger
    }
```

### Math Explanation

```latex
$C = S_0 \Phi(d_1) - X e^{-rT} \Phi(d_2)$
$P = X e^{-rT} \Phi(-d_2) - S_0 \Phi(-d_1)$

$d_1 = \frac{\ln(S_0 / X) + (r + \sigma^2 / 2)T}{\sigma \sqrt{T}}$
$d_2 = d_1 - \sigma \sqrt{T}$
```

### Explanation

- **Installation**: Provides step-by-step instructions for setting up the project.
- **Usage**: Describes how to run the application using Streamlit.
- **Project Structure**: Lists the directory structure of the project.
- **Testing**: Explains how to run the unit tests using `pytest`.
- **Contributing**: Provides guidelines for contributing to the project.
- **License**: States the project's license.

Feel free to adjust the content based on your project's specifics, such as the repository URL and any additional setup steps.

