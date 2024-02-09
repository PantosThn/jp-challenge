import os
import sys
# Get the path to the parent directory of the current directory (tests directory)
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Add the parent directory (project root) to the sys.path
sys.path.append(parent_dir)

import unittest
from datetime import datetime
from src.stock_utilities import StockData, StockType, TradeType
from datetime import datetime, timedelta


class TestStockData(unittest.TestCase):
    def setUp(self):
        self.tea_stock = StockData("TEA", StockType.COMMON, 0.0, None, 100.0)
        self.pop_stock = StockData("POP", StockType.COMMON, 8.0, None, 100.0)
        self.ale_stock = StockData("ALE", StockType.COMMON, 23.0, None, 60.0)
        self.gin_stock = StockData("GIN", StockType.PREFERRED, 8.0, 0.02, 100.0)
        self.joe_stock = StockData("JOE", StockType.COMMON, 13.0, None, 250.0)
        self.preferred_stock_no_dividend = StockData("XYZ", StockType.PREFERRED, 8.0, None, 100.0)
        self.stock = StockData("ABC", StockType.COMMON, 10.0, None, 100.0)

    def test_dividend_yield_common_stock(self):
        # Test dividend yield for common stocks with last dividend
        self.assertAlmostEqual(self.tea_stock.dividend_yield(10), 0.0)  # TEA
        self.assertAlmostEqual(self.tea_stock.dividend_yield(100), 0.0)  # TEA (price doesn't affect dividend yield)
        self.assertAlmostEqual(self.pop_stock.dividend_yield(100), 0.08) 
        self.assertAlmostEqual(self.ale_stock.dividend_yield(100), 0.23) 
        self.assertAlmostEqual(self.joe_stock.dividend_yield(100), 0.13) 

    def test_dividend_yield_preferred_stock(self):
        # Test dividend yield for preferred stocks with fixed dividend
        self.assertAlmostEqual(self.gin_stock.dividend_yield(100), (0.02 * 100) / 100)  # GIN
        # Test dividend yield for preferred stocks without fixed dividend
        with self.assertRaises(ValueError):
            self.preferred_stock_no_dividend.dividend_yield(100)  # XYZ

    def test_invalid_inputs(self):
        # Test invalid inputs
        with self.assertRaises(ValueError):
            self.tea_stock.dividend_yield(0)
        with self.assertRaises(ValueError):
            self.gin_stock.dividend_yield(0)
        with self.assertRaises(ValueError):
            self.preferred_stock_no_dividend.dividend_yield(100)

    def test_pe_ratio(self):
        # Test P/E ratio calculation
        
        # Test P/E ratio calculation for stock with zero dividend
        self.assertIsNone(self.tea_stock.pe_ratio(100))  # TEA

        # Test P/E ratio calculation for pop_stock (Common, dividend = 8)
        self.assertEqual(self.pop_stock.pe_ratio(100), 1250)  # P/E ratio = Price / Dividend

        # Test P/E ratio calculation for ale_stock (Common, dividend = 23)
        self.assertAlmostEqual(self.ale_stock.pe_ratio(100), (100 / 0.23))  # P/E ratio = Price / Dividend

        # Test P/E ratio calculation for gin_stock 
        self.assertEqual(self.gin_stock.pe_ratio(100), (100/0.02))  # P/E ratio = Price / Dividend

        # Test P/E ratio calculation for preferred_stock_no_dividend (Preferred, dividend = None)
        with self.assertRaises(ValueError):
           self.preferred_stock_no_dividend.pe_ratio(100)

    def test_trading(self):
        # Test various trading scenarios
        initial_trades_count = len(self.stock.trades)

        # Record a valid buy trade
        self.stock.record_trade(100, 50.0, TradeType.BUY)
        self.assertEqual(len(self.stock.trades), initial_trades_count + 1)
        last_trade = self.stock.trades[-1]
        self.assertEqual(last_trade['quantity'], 100)
        self.assertEqual(last_trade['price'], 50.0)
        self.assertEqual(last_trade['indicator'], TradeType.BUY)
        # Ensure the timestamp is recent (within a second)
        self.assertAlmostEqual((datetime.now() - last_trade['timestamp']).total_seconds(), 0, delta=1)

        # Record a valid sell trade
        self.stock.record_trade(50, 60.0, TradeType.SELL)
        self.assertEqual(len(self.stock.trades), initial_trades_count + 2)
        last_trade = self.stock.trades[-1]
        self.assertEqual(last_trade['quantity'], 50)
        self.assertEqual(last_trade['price'], 60.0)
        self.assertEqual(last_trade['indicator'], TradeType.SELL)

        # Test recording a trade with zero quantity
        with self.assertRaises(ValueError):
            self.stock.record_trade(0, 50.0, TradeType.BUY)

        # Test recording a trade with negative quantity
        with self.assertRaises(ValueError):
            self.stock.record_trade(-100, 50.0, TradeType.BUY)

        # Test recording a trade with zero price
        with self.assertRaises(ValueError):
            self.stock.record_trade(100, 0, TradeType.BUY)

        # Test recording a trade with negative price
        with self.assertRaises(ValueError):
            self.stock.record_trade(100, -50.0, TradeType.BUY)

        # Test recording a trade with an invalid indicator
        with self.assertRaises(ValueError):
            self.stock.record_trade(100, 50.0, "INVALID")

    def test_volume_weighted_stock_price_with_trades(self):
        # Test with trades within the last 15 minutes
        now = datetime.now()
        fifteen_minutes_ago = now - timedelta(minutes=15)

        # Create trades within the last 15 minutes
        self.stock.trades = [
            {'timestamp': now, 'quantity': 100, 'price': 50.0},
            {'timestamp': fifteen_minutes_ago, 'quantity': 200, 'price': 60.0}
        ]

        # Calculate volume-weighted stock price
        expected_price = (100 * 50.0 + 200 * 60.0) / (100 + 200)
        self.assertAlmostEqual(self.stock.volume_weighted_stock_price(), expected_price)

    def test_volume_weighted_stock_price_no_trades(self):
        # Test with no trades available
        self.assertIsNone(self.stock.volume_weighted_stock_price())

    def test_volume_weighted_stock_price(self):
       # Assuming some trades are recorded for the stocks
       self.tea_stock.record_trade(10, 100, TradeType.BUY)
       self.tea_stock.record_trade(5, 110, TradeType.SELL)
       self.gin_stock.record_trade(5, 120, TradeType.BUY)
       self.gin_stock.record_trade(10, 125, TradeType.SELL)

       # Test volume weighted stock price
       self.assertAlmostEqual(self.tea_stock.volume_weighted_stock_price(), 103.333, places=3) # ((10*100) + (5*110)) / (10 + 5)
       self.assertAlmostEqual(self.gin_stock.volume_weighted_stock_price(), 123.333, places=3)  # ((5*120) + (10*125)) / (5 + 10)


if __name__ == '__main__':
    unittest.main()