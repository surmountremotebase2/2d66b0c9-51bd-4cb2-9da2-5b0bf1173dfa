from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD, SO
from surmount.logging import log
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # This strategy focuses on the BTC/USD pair
        return ["BTC/USD"]

    @property
    def interval(self):
        # Choosing a daily interval for analysis
        return "1day"

    def run(self, data):
        # Initialize the volume and technical indicators for BTC/USD
        btc_data = data["ohlcv"]["BTC/USD"]
        volume = [i["volume"] for i in btc_data][-2:]
        rsi = RSI("BTC/USD", btc_data, length=14)[-1]
        macd_signal = MACD("BTC/USD", btc_data, fast=12, slow=26)["signal"][-1]
        macd_value = MACD("BTC/USD", btc_data, fast=12, slow=26)["MACD"][-1]
        stochastic = SO("BTC/USD", btc_data)[-1]

        btc_stake = 0

        # Define the buy signal based on volume increase, positive sentiment approximated by RSI, MACD, and stochastic conditions
        if volume[-1] > volume[-2] and rsi > 50 and macd_value > macd_signal and stochastic > 20:
            btc_stake = 1  # Consider going all in as a simple example
            
        # Similarly, define a sell signal based on decrease in volume or negative market sentiment
        elif volume[-1] < volume[-2] or rsi < 50 or macd_value < macd_signal or stochastic < 80:
            btc_stake = 0  # Exit the position

        log(f"BTC/USD Allocation: {btc_stake}")
        return TargetAllocation({"BTC/USD": btc_stake})