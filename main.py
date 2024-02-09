# Import necessary classes and libraries
from src.stock_utilities import StockData
from src.user_interactions import (
    get_stock_data_from_user,
    dividend_yield_interaction,
    pe_ratio_interaction,
    record_trade_interaction,
    volume_weighted_stock_price_interaction,
    gbce_all_share_index_interaction,
    get_user_input
)

def main():
    # Get stock data from user input
    symbol, stock_type, last_dividend, fixed_dividend, par_value = get_stock_data_from_user()

    # Create a StockData instance with the provided data
    stock = StockData(symbol, stock_type, last_dividend, fixed_dividend, par_value)

    # Define a dictionary mapping user input choices to corresponding functions
    menu = {
        "1": dividend_yield_interaction,
        "2": pe_ratio_interaction,
        "3": record_trade_interaction,
        "4": volume_weighted_stock_price_interaction,
        "5": gbce_all_share_index_interaction,
        "6": exit
    }
    # Main loop for user interactions
    while True:
        # Display menu options
        print("\nSelect an operation:")
        print("1. Calculate Dividend Yield")
        print("2. Calculate P/E Ratio")
        print("3. Record a Trade")
        print("4. Calculate Volume-weighted Stock Price")
        print("5. Calculate GBCE All Share Index")
        print("6. Exit")
        
        # Get user choice
        choice = get_user_input("\nEnter your choice: ")

        # Execute corresponding function based on user choice
        if choice in menu:
            menu[choice](stock)
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")

        # Ask user if they want to continue
        cont = get_user_input("\nDo you want to continue? (Y/N): ").upper()
        if cont != "Y":
            break

if __name__ == "__main__":
    main()