from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.logging import log
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    
    def __init__(self):
        self.ticker = "BTC-USD"  # Define the ticker symbol for Bitcoin
        self.data_list = [OHLCV(self.ticker)]

    @property
    def interval(self):
        # Use a 1-hour interval for intraday trading analysis
        return "1hour"

    @property
    def assets(self):
        # Define Bitcoin as the asset to trade
        return [self.ticker]

    @property
    def data(self):
        # Specify the data needed for the strategy
        return self.data_list

    def run(self, data):
        btc_data = data["ohlcv"]  # Access the OHLCV data for Bitcoin
        
        # Ensure there is enough data to calculate indicators
        if len(btc_data) < 14:
            return TargetAllocation({})
        
        rsi_values = RSI(self.ticker, btc_data, 14)  # Calculate the 14-period RSI for Bitcoin
        
        # Calculate the 10-period SMA of volume for Bitcoin
        volume_sma = SMA(self.ticker, [{"BTC-USD": {"volume": d["BTC-USD"]["volume"]}} for d in btc_data], 10)
        
        # Get the latest close price and volume
        latest_close = btc_data[-1]["BTC-USD"]["close"]
        latest_volume = btc_data[-1]["BTC-USD"]["volume"]
        
        btc_stake = 0  # Initialize the stake in Bitcoin as 0
        
        # Define the buy condition: RSI below 30 (oversold), current volume above SMA volume
        if rsi_values[-1] < 30 and latest_volume > volume_sma[-1]:
            log(f"Buying signal detected with RSI: {rsi_values[-1]} and Volume: {latest_volume}")
            btc_stake = 1  # Set the stake to 100% of the portfolio
        
        # Define the sell condition: RSI above 70 (overbought)
        elif rsi_values[-1] > 70:
            log(f"Selling signal detected with RSI: {rsi_values[-1]}")
            btc_stake = 0  # Reduce the stake to 0% of the portfolio

        return TargetAllocation({self.ticker: btc_stake})