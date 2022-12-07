from django.test import TestCase
import yfinance as yf

class yfinanceDataTest(TestCase):
    """ Pulls an ETF, confirms that the data is correct """
    def setUp(self):
        """ Create ETF info dict. """
        self.etf_info = yf.Ticker("BAB").info
        pass
    
    def test_symbol_correct(self):
        """ Has the right ETF been pulled? """
        self.assertEqual(self.etf_info["symbol"], "BAB")
    