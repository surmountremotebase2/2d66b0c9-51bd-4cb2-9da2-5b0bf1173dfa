from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset and RSI periods
        self.tickers = ["BTC"]
        self.rsi_period = 14  # Commonly used RSI period
        # Thresholds for identifying overbought and oversold conditions
        self.rsi_overbought = 70
        self.rsi_oversold = 30

    @property
    def assets(self):
        # Specify that this strategy applies to Bitcoin
        return self.tickers

    @property
    def interval(self):
        # Daily intervals commonly used for medium-long term trades
        return "1day"

    def run(self, data):
        # Compute RSI for Bitcoin
        btc_rsi = RSI("BTC", data["ohlcv"], self.rsi_period)
        
        # Initialize the allocation dictionary
        allocation_dict = {"BTC": 0}

        if len(btc_rsi) > 0:
            current_rsi = btc_rsi[-1]
            log("Current BTC RSI: {}".format(current_rsi))

            # If RSI indicates oversold, consider buying Bitcoin
            if current_rsi < self.rsi_oversold:
                log("Bitcoin appears oversold. Considering buying.")
                allocation_dict["BTC"] = 1  # Allocating 100% to Bitcoin
            
            # If RSI indicates overbought, consider selling Bitcoin
            elif current_rsi > self.rsi_overbought:
                log("Bitcoin appears overbought. Considering selling.")
                allocation_dict["BTC"] = 0  # Allocating 0% to Bitcoin (selling our position)
            
            # You can integrate risk management by adjusting allocation based on your risk tolerance and market analysis

        return TargetAllocation(allocation_dict)