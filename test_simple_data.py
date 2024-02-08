import unittest
from datetime import datetime
from simple_data import SimpleData, StockType


class TestSimpleData(unittest.TestCase):
    def setUp(self):
        # Create instances of SimpleData for testing
        self.common_stock = SimpleData("TEA", StockType.COMMON, 0.0, None, 100.0)
        self.preferred_stock = SimpleData("GIN", StockType.PREFERRED, 8.0, 0.02, 100.0)

    def test_dividend_yield(self):
        # Test dividend yield for common stock
        self.assertEqual(self.common_stock.dividend_yield(100), 0.0)
        self.assertEqual(self.common_stock.dividend_yield(50), 0.0)  # Assuming last_dividend is 0

        # Test dividend yield for preferred stock
        self.assertEqual(self.preferred_stock.dividend_yield(100), 0.02)
        self.assertEqual(self.preferred_stock.dividend_yield(50), 0.04)

        # Test dividend yield when price is 0
        with self.assertRaises(ValueError):
            self.common_stock.dividend_yield(0)
        with self.assertRaises(ValueError):
            self.preferred_stock.dividend_yield(0)

    def test_pe_ratio(self):
        # Test P/E ratio for common stock
        with self.assertRaises(ValueError):
            self.common_stock.pe_ratio(0)
        self.assertEqual(self.common_stock.pe_ratio(100), None)  # Assuming last_dividend is 0

        # Test P/E ratio for preferred stock
        self.assertEqual(self.preferred_stock.pe_ratio(100), 5000.0)
        self.assertEqual(self.preferred_stock.pe_ratio(50), 1250.0)

        # Test P/E ratio when dividend is 0
        self.assertIsNone(self.common_stock.pe_ratio(100))

    def test_record_trade(self):
        # Record a trade for common stock
        self.common_stock.record_trade(10, 100, 'BUY')
        self.assertEqual(len(self.common_stock.trades), 1)

        # Record a trade for preferred stock
        self.preferred_stock.record_trade(5, 120, 'SELL')
        self.assertEqual(len(self.preferred_stock.trades), 1)

        # Check if trade record has correct data
        trade = self.common_stock.trades[0]
        self.assertIsInstance(trade['timestamp'], datetime)
        self.assertEqual(trade['quantity'], 10)
        self.assertEqual(trade['price'], 100)
        self.assertEqual(trade['indicator'], 'BUY')

    def test_volume_weighted_stock_price(self):
        # Assuming some trades are recorded for the stocks
        self.common_stock.record_trade(10, 100, 'BUY')
        self.common_stock.record_trade(5, 110, 'SELL')
        self.preferred_stock.record_trade(5, 120, 'BUY')
        self.preferred_stock.record_trade(10, 125, 'SELL')

        # Test volume weighted stock price
        self.assertAlmostEqual(self.common_stock.volume_weighted_stock_price(), 103.333, places=3) # ((10*100) + (5*110)) / (10 + 5)
        self.assertAlmostEqual(self.preferred_stock.volume_weighted_stock_price(), 123.333, places=3)  # ((5*120) + (10*125)) / (5 + 10)


if __name__ == '__main__':
    unittest.main()