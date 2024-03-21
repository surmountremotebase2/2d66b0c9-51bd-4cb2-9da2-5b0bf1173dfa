from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV, Asset

class DCAInvestmentStrategy(Strategy):
    def __init__(self):
        # Define the stocks of interest
        self.stocks = ["AAPL", "NVDA"]
        # Monthly budget for investment in USD
        self.monthly_budget = 1000  # This could be adjusted based on your investment capacity
        # Allocate the budget evenly across the stocks
        self.stock_allocation_budget = self.monthly_budget / len(self.stocks)

    @property
    def assets(self):
        # Return the list of stocks the strategy will operate on
        return self.stocks

    @property
    def interval(self):
        # Based on the platform's operation, this might need to be "1month" for monthly DCA
        # or "1quarter" if it supports quarterly operations, otherwise select the closest option.
        return "1month"

    def run(self, data):
        # This example doesn't factor in stock prices because DCA executes regardless of price.
        # The placeholder 0.5 for each stock implies an even split, not an actual quantity or percentage of budget.
        # This should be converted into actual orders based on current stock prices and the defined budget within a trading execution environment.
        allocation = {stock: 0.5 for stock in self.stocks}

        return TargetAllocation(allocation)

# Note: This simplified strategy does not include actual trading/order execution logic.
# Real-world implementation on the Surmount AI platform or any trading system would require further integration for executing trades based on this allocation, considering the current stock prices to calculate the number of shares to buy within the given budget.