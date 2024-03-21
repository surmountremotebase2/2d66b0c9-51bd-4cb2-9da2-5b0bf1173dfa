from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading

class TradingStrategy(Strategy):

    # Define initialization parameters if necessary
    def __init__(self):
        self.tickers = ["AAPL", "MSFT"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"
    
    @property
    def data(self):
        # Here you would specify the data you want preloaded before your strategy runs.
        # For instance, InstitutionalOwnership and InsiderTrading as in the examples, or none if unnecessary.
        return []

    def run(self, data):
        # This is where you would use the data parameter, which contains historical data.
        # For example, to access 'close' price of 'AAPL', you would do something like:
        # close_prices = [d["AAPL"]["close"] for d in data["ohlcv"]]
        # Then, you can apply your logic based on the accessed data and indicators.

        # Placeholder for allocation logic. For example: equally invest in all tickers.
        allocation_dict = {ticker: 1/len(self.tickers) for ticker in self.tickers}

        return TargetAllocation(allocation_dict)