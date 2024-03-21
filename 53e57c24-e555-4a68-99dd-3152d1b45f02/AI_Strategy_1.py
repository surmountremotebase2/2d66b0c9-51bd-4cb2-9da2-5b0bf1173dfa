from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log
from surmount.data import Asset, OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset symbol for Bitcoin in the format used by your data provider
        self.asset_symbol = "BTC-USD"
        # This example doesn't directly fetch data from Polygon.io API but assumes
        # market data for Bitcoin is available through the OHLCV class or an equivalent
        self.data_list = [OHLCV(self.asset_symbol)]

    @property
    def interval(self):
        # Set the interval for RSI calculation - "1day" is used for daily RSI analysis
        return "1day"

    @property
    def assets(self):
        # List of assets (in this case, only Bitcoin) that the strategy focuses on
        return [self.asset_symbol]

    @property
    def data(self):
        # Data required for the strategy, assumed to be provided or fetched from Polygon.io
        return self.data_list

    def run(self, data):
        # Initialize the target allocation for Bitcoin as 0 (no position)
        btc_allocation = 0

        # Calculate the RSI for Bitcoin with a period of 14 days
        btc_rsi = RSI(self.asset_symbol, data["ohlcv"], 14)
        
        if btc_rsi is None or len(btc_rsi) < 14:
            # Not enough data available to calculate RSI; no trading decision made
            log("Insufficient data for RSI calculation.")
            return TargetAllocation({})
        
        latest_rsi = btc_rsi[-1]
        log(f"Latest RSI for {self.asset_symbol}: {latest_rsi}")

        # Determine trading action based on RSI value
        if latest_rsi < 30:
            # RSI indicates oversold conditions; consider buying Bitcoin
            btc_allocation = 1  # 100% of the portfolio allocated to buying Bitcoin
            log("RSI < 30: Buying signal.")
        elif latest_rsi > 70:
            # RSI indicates overbought conditions; consider selling Bitcoin
            btc_allocation = -1  # Assuming short selling is allowed; otherwise, adjust accordingly
            log("RSI > 70: Selling signal.")

        # Return the target allocation for Bitcoin based on RSI analysis
        return TargetAllocation({self.asset_symbol: btc_allocation})

# It's crucial to remember that the actual execution of buy/sell orders and interaction with the Polygon.io API
# to fetch real-time market data requires additional implementation not covered in this Surmount AI strategy example.