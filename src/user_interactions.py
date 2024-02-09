import os
import logging
from src.stock_utilities import StockType, TradeType, GBCECalculator

# Configure logging
logs_directory='logs'
os.makedirs(logs_directory, exist_ok=True)
log_file_path = os.path.join(logs_directory, 'user_interaction.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_input(prompt):
    """
    Get user input with a prompt and log the input.
    
    Args:
        prompt (str): The prompt message for user input.
    
    Returns:
        str: The user input.
    """
    user_input = input(prompt).strip()
    logging.info(f"User input: {prompt.strip()} - {user_input}")
    return user_input

def get_float_input(prompt):
    """
    Get user input as a float value.
    
    Args:
        prompt (str): The prompt message for user input.
    
    Returns:
        float: The user input as a float value.
    """
    while True:
        user_input = get_user_input(prompt)
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_stock_data_from_user():
    """
    Get stock data from user input.
    
    Returns:
        tuple: A tuple containing symbol, stock_type, last_dividend, fixed_dividend, and par_value.
    """
    symbol = get_user_input("Enter the symbol of the stock: ")
    stock_type_input = get_user_input("Enter the type of the stock (COMMON/PREFERRED): ").upper()
    while stock_type_input not in ["COMMON", "PREFERRED"]:
        print("Invalid stock type. Please enter COMMON or PREFERRED.")
        stock_type_input = get_user_input("Enter the type of the stock (COMMON/PREFERRED): ").upper()
    stock_type = StockType[stock_type_input]
    
    # Validate last dividend for common stock or fixed dividend for preferred stock
    if stock_type == StockType.COMMON:
        last_dividend = None
        while last_dividend is None or last_dividend < 0:
            last_dividend = get_float_input("Enter the last dividend paid by the stock (it should not be negative): ")
            if last_dividend < 0:
                print("Last dividend must not be negative.")
        fixed_dividend = None
    elif stock_type == StockType.PREFERRED:
        fixed_dividend = None
        while fixed_dividend is None or fixed_dividend < 0:
            fixed_dividend = get_float_input("Enter the fixed dividend rate for preferred stocks (percentage eg 0.02 for 2%, it should not be negative): ")
            if fixed_dividend < 0:
                print("Fixed dividend must not be negative.")
        last_dividend = None

    par_value = None
    while par_value is None or par_value <= 0:
        par_value = get_float_input("Enter the par value of the stock (must be above zero): ")
        if par_value <= 0:
            print("Par value must be above zero.")
    return symbol, stock_type, last_dividend, fixed_dividend, par_value


def dividend_yield_interaction(stock):
    """
    Calculate and print the dividend yield for a given stock.
    
    Args:
        stock (StockData): The stock for which to calculate the dividend yield.
    """
    try:
        price = get_float_input("Enter the current price of the stock: ")
        logging.info(f"User input - Operation: Calculate Dividend Yield - Price: {price}")
        result = stock.dividend_yield(price)
        print("\nDividend Yield:", result)
        logging.info(f"Calculation Result - Dividend Yield: {result}")
    except ValueError  as e:
        print("\nError:", e)
        logging.error(f"Error: {e}")

def pe_ratio_interaction(stock):
    """
    Calculate and print the P/E ratio for a given stock.
    
    Args:
        stock (StockData): The stock for which to calculate the P/E ratio.
    """
    try:
        price = get_float_input("Enter the current price of the stock: ")
        logging.info(f"User input - Operation: Calculate P/E Ratio - Price: {price}")
        result = stock.pe_ratio(price)
        if result is not None:
            print("\nP/E Ratio:", result)
            logging.info(f"Calculation Result - P/E Ratio: {result}")
        else:
            print("\nP/E Ratio cannot be calculated because dividend is zero.")
            logging.info("Calculation Result - P/E Ratio cannot be calculated because dividend is zero.")
    except ValueError  as e:
        print("\nError:", e)
        logging.error(f"Error: {e}")

def record_trade_interaction(stock):
    """
    Record a trade for a given stock.
    
    Args:
        stock (StockData): The stock for which to record the trade.
    """
    try:
        quantity = int(get_user_input("Enter the quantity of shares traded: "))
        price = get_float_input("Enter the price at which the trade occurred: ")
        indicator_input = get_user_input("Enter whether the trade is a buy or sell (BUY/SELL): ").upper()
        while indicator_input not in ["BUY", "SELL"]:
            print("Invalid trade indicator. Please enter BUY or SELL.")
            indicator_input = get_user_input("Enter whether the trade is a buy or sell (BUY/SELL): ").upper()
        indicator = TradeType[indicator_input]
        stock.record_trade(quantity, price, indicator)
        print("\nTrade recorded successfully")
        logging.info(f"User input - Operation: Record Trade - Quantity: {quantity}, Price: {price}, Indicator: {indicator}")
        logging.info("Trade recorded successfully")
    except ValueError  as e:
        print("\nError:", e)
        logging.error(f"Error: {e}")

def volume_weighted_stock_price_interaction(stock):
    """
    Calculate and print the volume-weighted stock price for a given stock.
    
    Args:
        stock (StockData): The stock for which to calculate the volume-weighted stock price.
    """
    result = stock.volume_weighted_stock_price()
    if result is not None:
        print("\nVolume-weighted Stock Price:", result)
        logging.info(f"Calculation Result - Volume-weighted Stock Price: {result}")
    else:
        print("\nNo trades within the last 15 minutes.")
        logging.info("No trades within the last 15 minutes.")

def gbce_all_share_index_interaction(stock):
    result = GBCECalculator.calculate_gbce_all_share_index([stock])
    if result is not None:
        print("\nGBCE All Share Index:", result)
        logging.info(f"Calculation Result - GBCE All Share Index: {result}")
    else:
        print("\nNo valid stocks with trades.")
        logging.info("No valid stocks with trades.")

