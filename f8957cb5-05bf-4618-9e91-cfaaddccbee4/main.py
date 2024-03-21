from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, OBV
from surmount.logging import log
from surmount.data import Asset, InsiderTrading
import pandas_ta as ta
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker for Meta Platforms, Inc. (previously known as Facebook) for clarity.
        self.ticker = "META"
        # Insider trading data might signal significant selling pressure from insiders.
        self.data_list = [InsiderTrading(self.ticker)]

    @property
    def interval(self):
        # Daily interval to analyze the overall trend and significant daily movements.
        return "1day"

    @property
    def assets(self):
        # Focus solely on Meta's stock for this strategy.
        return [self.ticker]

    @property
    def data(self):
        # Data requirement for this strategy includes insider trading data.
        return self.data_list

    def run(self, data):
        # Start with a neutral perspective, not holding META.
        allocation_dict = {self.ticker: 0}
        
        # Check the most recent insider trading activities for sales.
        recent_insider_activity = data[("insider_trading", self.ticker)]
        sales_detected = False
        for activity in recent_insider_activity:
            if "Sale" in activity['transactionType']:
                sales_detected = True
                log("Significant insider selling detected.")
                break
                
        # Calculate the short term and long term moving average to identify market downturns.
        sma_short_term = SMA(self.ticker, data["ohlcv"], 20)  # 20-day SMA for the short term
        sma_long_term = SMA(self.ticker, data["ohlcv"], 50)  # 50-day SMA for the long term
        
        # Calculate On-Balance Volume to understand volume flow and potentially detect selling pressure.
        obv_values = OBV(self.ticker, data["ohlcv"])
        
        if len(sma_short_term) > 0 and len(sma_long_term) > 0 and len(obv_values) > 0:
            # Identify a market downturn for META and significant selling pressure.
            if sma_short_term[-1] < sma_long_term[-1] and obv_values[-1] < ta.sma(pd.Series(obv_values), 20).iloc[-1] and sales_detected:
                # If both conditions are met, move to sell position for META.
                allocation_dict[self.ticker] = 0  # Represents selling off META holdings.
                log("Selling META due to market downturn and detected selling pressure.")
            else:
                # Stay neutral if the conditions do not meet our criteria for selling.
                allocation_dict[self.ticker] = 0  # Keep holding position as is, assuming initial position is neutral.
                log("Conditions not met for selling META.")
        
        return TargetAllocation(allocation_dict)