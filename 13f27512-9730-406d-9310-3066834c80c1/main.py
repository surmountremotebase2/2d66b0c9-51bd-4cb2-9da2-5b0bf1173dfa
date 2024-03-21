from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    @property
    def assets(self):
        # Define the assets we are interested in.
        return ["PFE", "NVDA"]
    
    @property
    def interval(self):
        # We set the interval as 1 hour to check the conditions several times throughout the trading day.
        return "1hour"
    
    def run(self, data):
        # Initialize the stake for both TQQQ and SPY to 0.
        tqqq_stake = 0
        spy_stake = 0

        # Access the OHLCV data for our assets.
        d = data["ohlcv"]

        if len(d) > 3:
            # We are looking to buy TQQQ midday.
            if "13:00" in d[-1]["TQQQ"]["date"]:
                # A dip is identified when the current close is lower than the previous close.
                if d[-1]["TQQQ"]["close"] < d[-2]["TQQQ"]["close"]:
                    # Define the stake for TQQQ if there is a dip. Here, we attempt to buy.
                    tqqq_stake = 0.5 # Using 50% of available capital for simplicity.

            # Conditions to sell TQQQ at the end of the day and hold SPY with remaining capital.
            if "16:00" in d[-1]["TQQQ"]["date"]:
                # Reset TQQQ stake to 0, indicating selling it off.
                tqqq_stake = 0
                # With the remaining capital, we invest in SPY. 
                spy_stake = 1 - tqqq_stake # Assuming whatever is not allocated to TQQQ goes to SPY.
        
        # We create a dictionary with our allocations.
        allocation_dict = {"TQQQ": tqqq_stake, "SPY": spy_stake}
        # Return our target allocation.
        return TargetAllocation(allocation_dict)