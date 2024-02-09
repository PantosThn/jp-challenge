from enum import Enum
from datetime import datetime, timedelta
from operator import mul
from functools import reduce

class StockType(Enum):
    COMMON = "COMMON"
    PREFERRED = "PREFERRED"

class TradeType(Enum):
    BUY = "BUY"
    SELL = "SELL"

class StockData:
    def __init__(self, symbol: str, stock_type: StockType, last_dividend: float, fixed_dividend: float, par_value: float):
        """
        Initialize a SimpleData object with the given parameters.

        :param symbol: The symbol of the stock.
        :param stock_type: The type of the stock (COMMON or PREFERRED).
        :param last_dividend: The last dividend paid by the stock.
        :param fixed_dividend: The fixed dividend rate for preferred stocks (percentage).
        :param par_value: The par value of the stock.
        """
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = []
        
    def dividend_yield(self, price):
        """
        Calculate the dividend yield for the stock.

        Args:
            price (float): The current price of the stock.

        Returns:
            float: The calculated dividend yield.
            
        Raises:
            ValueError: If the price is non-positive, if the last dividend is non-positive,
                        if the fixed dividend is non-positive for preferred stocks, or if the price is zero.
        """
        if price <= 0:
            raise ValueError("Price must be positive")
        
        if self.stock_type == StockType.COMMON:
            if self.last_dividend is None or self.last_dividend < 0:
                raise ValueError("Last dividend must be provided and be positive for Common stocks")
            return self.last_dividend / price
        
        elif self.stock_type == StockType.PREFERRED:
            if self.fixed_dividend is None or self.fixed_dividend <= 0:
                raise ValueError("Fixed dividend must be provided and to be positive for Preferred stocks")
            return (self.fixed_dividend * self.par_value) / price

    def pe_ratio(self, price):
        """
        Calculate the price-to-earnings (P/E) ratio.

        Args:
            price (float): The current price of the stock.

        Returns:
            float or None: The calculated P/E ratio, or None if the dividend is zero.
        """
        # Calculate dividend yield
        dividend = self.dividend_yield(price)
        
        # Return None if the dividend is zero, indicating that the P/E ratio cannot be calculated
        if dividend == 0:
            return None
        
        # Calculate and return P/E ratio
        return price / dividend


    def record_trade(self, quantity: int, price: float, indicator: TradeType):
        """
        Record a trade for the stock.

        Args:
            quantity (int): The quantity of shares traded.
            price (float): The price at which the trade occurred.
            indicator (TradeType): Indicator whether the trade is a buy or sell.

        Returns:
            None
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if price <= 0:
            raise ValueError("Price must be positive")
        if indicator not in TradeType:
            raise ValueError("Invalid trade indicator")

        timestamp = datetime.now()
        self.trades.append({'timestamp': timestamp, 'quantity': quantity, 'price': price, 'indicator': indicator})

    def volume_weighted_stock_price(self):
        """
        Calculate the volume-weighted stock price based on trades within the last 15 minutes.

        Returns:
            float or None: The volume-weighted stock price, or None if there are no trades within the last 15 minutes.
        """
        # Calculate the timestamp 15 minutes ago
        fifteen_minutes_ago = datetime.now() - timedelta(minutes=15)

        # Filter trades within the last 15 minutes
        trades_within_15_minutes = [trade for trade in self.trades if trade['timestamp'] >= fifteen_minutes_ago]

        # If no trades within the last 15 minutes, return None
        if not trades_within_15_minutes:
            return None

        # Calculate total value and total quantity for volume-weighted stock price
        total_value = sum(trade['price'] * trade['quantity'] for trade in trades_within_15_minutes)
        total_quantity = sum(trade['quantity'] for trade in trades_within_15_minutes)

        # Calculate volume-weighted stock price
        return total_value / total_quantity


class GBCECalculator:
    @staticmethod
    def calculate_gbce_all_share_index(stock_data):
        """
        Calculate the GBCE All Share Index using the geometric mean of prices for all valid stocks.

        Args:
            stock_data (list): A list of stock data, each element containing information about a stock.

        Returns:
            float or None: The calculated GBCE All Share Index, or None if there are no valid stocks with trades.
        """
        if not stock_data:
            return None  # Handle case when stock_data is empty

        # Filter out stocks without any trades
        valid_stocks = [stock for stock in stock_data if stock.trades]

        if not valid_stocks:
            return None  # Handle case when all stocks have no trades

        # Calculate the product of prices for valid stocks
        prices = [stock.trades[-1]['price'] for stock in valid_stocks]
        product = reduce(mul, prices, 1)

        # Calculate the geometric mean of prices for all valid stocks
        return (product) ** (1.0 / len(valid_stocks))