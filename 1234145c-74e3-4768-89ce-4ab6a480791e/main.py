from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import InstitutionalOwnership, InsiderTrading, FinancialStatement

class TradingStrategy(Strategy):
    def __init__(self):
        # A predefined list of tickers to exclude, ideally determined by sector analysis outside of this code.
        # This list should contain tickers related to the beer, wine, and liquor sectors.
        self.exclude_tickers = ["BEER", "WINE", "LIQR"]  # Placeholder tickers for example
        # Assuming 'SP500_tickers' is a list of S&P 500 tickers obtained from an external source
        self.tickers = [ticker for ticker in SP500_tickers if ticker not in self.exclude_tickers]  
        self.data_list = [FinancialStatement(ticker) for ticker in self.tickers]

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
        # This example strategy equally weights the remaining S&P 500 equities after exclusions
        num_assets = len(self.tickers)
        if num_assets == 0:
            log("No eligible assets to trade.")
            return TargetAllocation({})
        allocation_per_asset = 1 / num_assets
        allocation_dict = {ticker: allocation_per_asset for ticker in self.tickers}

        return TargetAllocation(allocation_dict)