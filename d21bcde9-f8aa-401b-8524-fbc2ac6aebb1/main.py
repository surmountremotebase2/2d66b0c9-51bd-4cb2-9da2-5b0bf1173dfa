from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.logging import log
import pandas_ta as ta
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers for vaccine companies
        self.tickers = ["MRNA", "PFE", "BNTX", "AZN", "JNJ"]
        # Assuming VolumeData and SentimentData are custom data classes 
        # that fetch volume and sentiment data respectively
        self.data_list = [VolumeData(ticker) for ticker in self.tickers] 
        self.data_list += [SentimentData(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            volume_data_key = ('volume_data', ticker)  # Key format based on provided examples
            sentiment_data_key = ('sentiment_data', ticker)

            if volume_data_key in data and sentiment_data_key in data:
                avg_volume = ta.sma(pd.Series([i["volume"] for i in data[volume_data_key]]), length=14).iloc[-1]
                avg_sentiment = ta.sma(pd.Series([i["sentiment"] for i in data[sentiment_data_key]]), length=7).iloc[-1]
                
                # Buy signal: If average volume and sentiment exceed thresholds
                if avg_volume > 1.5 and avg_sentiment > 0.7:
                    allocation_dict[ticker] = 1.0 / len(self.tickers)
                # Sell signal: Implemented as reducing allocation to 0 for simplicity
                elif avg_volume < 1.5 and avg_sentiment < 0.7:
                    allocation_dict[ticker] = 0
                else:
                    # Maintain current allocation if neither condition is met
                    # Assuming a method to get current allocation (not demonstrated here)
                    allocation_dict[ticker] = self.get_current_allocation(ticker)

        # Normalize allocations to ensure the sum is within [0, 1]
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {ticker: allocation / total_allocation for ticker, allocation in allocation_dict.items()}
        
        return TargetAllocation(allocation_dict)

    def get_current_allocation(self, ticker):
        # Placeholder method to get current allocation for a ticker
        # Actual implementation would require accessing current portfolio state
        return 0.2  # Example fixed return value for demonstration