from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self, bollinger_period=20, std_dev=2, buy_percentage=0.1, buy_interval='weekly'):
        """
        Initialize the DCA strategy with Bollinger Bands for Bitcoin trading.

        :param bollinger_period: The number of days for calculating the Bollinger Bands.
        :param std_dev: The number of standard deviations for the bands.
        :param buy_percentage: The percentage of capital to invest in each purchase.
        :param buy_interval: Frequency of purchases ('weekly', 'monthly').
        """
        self.bollinger_period = bollinger_period
        self.std_dev = std_dev
        self.buy_percentage = buy_percentage
        self.buy_interval = buy_interval
        self.asset = 'BTC'
        
        self.last_buy_date = None  # Keeps track of the last purchase date

    @property
    def assets(self):
        """Defines the asset to trade. In this case, Bitcoin (BTC)."""
        return [self.asset]

    @property
    def interval(self):
        """Defines the observation interval for the strategy."""
        return "1day"

    def run(self, data):
        """
        Executes trading logic at specified intervals.

        :param data: The market data.
        :return: TargetAllocation object with the desired asset allocation.
        """
        current_date = pd.to_datetime(data["ohlcv"][-1][self.asset]["date"])
        current_close_price = data["ohlcv"][-1][self.asset]["close"]
        bollinger_bands = BB(self.asset, data["ohlcv"], self.bollinger_period, self.std_dev)

        # Check if it's time to buy based on the interval
        if self.last_buy_date is not None:
            if self.buy_interval == 'weekly' and (current_date - self.last_buy_date).days < 7:
                return TargetAllocation({})
            elif self.buy_interval == 'monthly' and (current_date - self.last_buy_date).days < 30:
                return TargetAllocation({})

        allocation = 0
        # If current close price is below the lower Bollinger band, buy.
        if current_close_price < bollinger_bands['lower'][-1]:
            log(f"Buying BTC at {current_close_price} on {current_date}, below lower Bollinger Band.")
            allocation = self.buy_percentage
            self.last_buy_date = current_date

        return TargetAllocation({self.asset: allocation})