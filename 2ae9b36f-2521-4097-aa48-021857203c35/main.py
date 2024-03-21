from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD, SO as Stochastics  # SO is stochastics
from surmount.logging import log
from surmount.data import Asset, Ohlcv

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming 'PHARM' is a placeholder for actual pharmaceutical sector tickers
        self.tickers = ["PHARMA1", "PHARMA2", "PHARMA3"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Define the interval for the data fetching
        return "1day"

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            volume_trend = self._is_volume_increasing(data["ohlcv"], ticker)
            market_sentiment = self._is_market_sentiment_positive(data["ohlcv"], ticker)
            rsi = RSI(ticker, data["ohlcv"], 14)[-1]  # Last item in RSI series
            macd_output = MACD(ticker, data["ohlcv"], 12, 26)
            macd = macd_output["MACD"][-1]  # Last value of MACD
            macd_signal = macd_output["signal"][-1]  # Last value of MACD signal line
            stochastics = Stochastics(ticker, data["ohlcv"])[-1]  # Last value of Stochastics

            if (volume_trend and market_sentiment and rsi > 50 and macd > macd_signal and stochastics > 20):
                # Buy signal
                allocation = 1 / len(self.tickers)  # Equally distribute allocation among tickers
            elif (not volume_trend and not market_sentiment and rsi < 50 and macd < macd_signal and stochastics < 80):
                # Sell signal, allocate 0
                allocation = 0
            else:
                # Neutral, maintain current allocation
                allocation = -1  # -1 indicates no change, for illustration purposes

            allocation_dict[ticker] = allocation

        # Filter out tickers that have no change in allocation (illustrative purpose)
        final_allocations = {k: v for k, v in allocation_dict.items() if v != -1}

        return TargetAllocation(final_allocations)

    def _is_volume_increasing(self, ohlcv, ticker):
        # Implement logic to check if volume is increasing
        return True  # Placeholder

    def _is_market_sentiment_positive(self, ohlcv, ticker):
        # Implement logic to check if market sentiment is positive
        return True  # Placeholder