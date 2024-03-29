# Stock Management System

This project aims to develop a stock management system that allows users to perform various operations such as calculating dividend yield, price-to-earnings (P/E) ratio, recording trades, and calculating volume-weighted stock price and GBCE All Share Index.

## Features

- **Dividend Yield Calculation:** Users can calculate the dividend yield for a given stock based on its type and current price.
- **P/E Ratio Calculation:** Users can calculate the price-to-earnings (P/E) ratio for a given stock based on its type and current price.
- **Trade Recording:** Users can record trades for a given stock, specifying the quantity, price, and whether it is a buy or sell trade.
- **Volume-weighted Stock Price:** Users can calculate the volume-weighted stock price based on trades within the last 15 minutes.
- **GBCE All Share Index:** Users can calculate the GBCE All Share Index using the geometric mean of prices for all valid stocks.

## Usage

To use the stock management system, follow these steps:

1. Clone the repository to your local machine:

2. Navigate to the project directory:

3. Run the main script:
   ```
   python main.py
   ```
5. Follow the on-screen prompts to perform various operations such as calculating dividend yield, recording trades, etc.

6. Run the unit tests if you would like:
   ```
   pytest tests/test_stock_utilities.py
   ``` 
You should also be able to see in the log folder the user input as well as the values calculated.

## Directory Structure

- **src:** Contains the source code for the stock management system.
- **tests:** Contains unit tests for the stock management system.
- **logs:** Contains log files for user interactions and calculations.

## Requirements

- Python 3.x
- Packages listed in `requirements.txt`

## License

This project is licensed under the [MIT License](LICENSE).
