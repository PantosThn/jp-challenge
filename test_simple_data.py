import unittest
from datetime import datetime
from stock_utilities import StockData, StockType, TradeType
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

        #self.assertAlmostEqual(self.stock.volume_weighted_stock_price(), expected_price)
    #def test_dividend_yield(self):
    #    # Test dividend yield for common stock
    #    self.assertEqual(self.common_stock.dividend_yield(100), 0.0)
    #    self.assertEqual(self.common_stock.dividend_yield(50), 0.0)  # Assuming last_dividend is 0
#
    #    # Test dividend yield for preferred stock
    #    self.assertEqual(self.preferred_stock.dividend_yield(100), 0.02)
    #    self.assertEqual(self.preferred_stock.dividend_yield(50), 0.04)
#
    #    # Test dividend yield when price is 0
    #    with self.assertRaises(ValueError):
    #        self.common_stock.dividend_yield(0)
    #    with self.assertRaises(ValueError):
    #        self.preferred_stock.dividend_yield(0)
#
    #def test_pe_ratio(self):
    #    # Test P/E ratio for common stock
    #    with self.assertRaises(ValueError):
    #        self.common_stock.pe_ratio(0)
    #    self.assertEqual(self.common_stock.pe_ratio(100), None)  # Assuming last_dividend is 0
#
    #    # Test P/E ratio for preferred stock
    #    self.assertEqual(self.preferred_stock.pe_ratio(100), 5000.0)
    #    self.assertEqual(self.preferred_stock.pe_ratio(50), 1250.0)
#
    #    # Test P/E ratio when dividend is 0
    #    self.assertIsNone(self.common_stock.pe_ratio(100))
#
    #def test_record_trade(self):
    #    # Record a trade for common stock
    #    self.common_stock.record_trade(10, 100, 'BUY')
    #    self.assertEqual(len(self.common_stock.trades), 1)
#
    #    # Record a trade for preferred stock
    #    self.preferred_stock.record_trade(5, 120, 'SELL')
    #    self.assertEqual(len(self.preferred_stock.trades), 1)
#
    #    # Check if trade record has correct data
    #    trade = self.common_stock.trades[0]
    #    self.assertIsInstance(trade['timestamp'], datetime)
    #    self.assertEqual(trade['quantity'], 10)
    #    self.assertEqual(trade['price'], 100)
    #    self.assertEqual(trade['indicator'], 'BUY')
#
    def test_volume_weighted_stock_price(self):
       # Assuming some trades are recorded for the stocks
       self.tea_stock.record_trade(10, 100, TradeType.BUY)
       self.tea_stock.record_trade(5, 110, TradeType.SELL)
       #self.tea_stock.record_trade(5, 120, TradeType.BUY)
       #self.tea_stock.record_trade(10, 125, TradeType.SELL)

       # Test volume weighted stock price
       self.assertAlmostEqual(self.tea_stock.volume_weighted_stock_price(), 103.333, places=3) # ((10*100) + (5*110)) / (10 + 5)
      # self.assertAlmostEqual(self.preferred_stock.volume_weighted_stock_price(), 123.333, places=3)  # ((5*120) + (10*125)) / (5 + 10)


if __name__ == '__main__':
    unittest.main()