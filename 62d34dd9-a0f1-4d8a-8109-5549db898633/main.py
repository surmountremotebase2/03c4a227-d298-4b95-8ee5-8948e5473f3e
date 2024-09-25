from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, InsiderTrading
from surmount.technical_indicators import ATR  # Average True Range for volatility
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming 'ITSLA' is an inverse asset to Tesla for demonstration purposes
        self.tickers = ["TSLA", "ITSLA"]  
        self.data_list = [InsiderTrading("TSLA")]  # Monitoring Tesla's Insider Trading as a part of our strategy inputs

    @property
    def interval(self):
        # Using daily data to assess volatility
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Utilizing Average True Range (ATR) as a measure of volatility
        # The calculation requires 'ohlcv' data provided by the Surmount platform implicitly
        tsla_atr = ATR("TSLA", data["ohlcv"], 14)  # 14-days ATR for TSLA

        # Decision making based on volatility threshold
        # Set thresholds based on historical data analysis and financial goals
        high_volatility_threshold = 10  # Assuming a threshold for high volatility; this value is hypothetical

        # Initial allocation assumes equal weight
        allocation_dict = {"TSLA": 0.5, "ITSLA": 0.5}

        # Check if the latest ATR value exceeds our predefined high volatility threshold
        if tsla_atr and len(tsla_atr) > 0 and tsla_atr[-1] > high_volatility_threshold:
            log("High Tesla volatility detected. Adjusting allocations.")
            # Increase allocation in the inverse asset to hedge against high volatility
            allocation_dict["TSLA"] = 0.25  # Reducing Tesla's allocation
            allocation_dict["ITSLA"] = 0.75  # Increasing inverse asset's allocation

            return TargetAllocation(allocation_dict)

        # If volatility is within acceptable range, maintain initial allocation
        return TargetAllocation(allocation_dict)