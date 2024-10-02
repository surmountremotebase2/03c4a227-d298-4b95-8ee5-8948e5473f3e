from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from datetime import timedelta, datetime

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets you are interested in
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA"]
        # OHLCV historical data for computing gainers, no need to add to data_list directly
        # as the strategy base class handles it based on the assets and interval properties

    @property
    def assets(self):
        # Return the list of assets the strategy is interested in
        return self.tickers

    @property
    def interval(self):
        # Use '1day' for daily changes, ensures we can check previous day's close to open
        return "1day"

    def select_top_gainers(self, yesterday_data):
        # Calculates the percentage change from open to close for each asset and selects top 3
        gainers = []
        for ticker in self.tickers:
            try:
                data = yesterday_data[ticker]
                open_price = data['open']
                close_price = data['close']
                if close_price is not None and open_price is not None and open_price > 0:
                    percent_change = (close_price - open_price) / open_price
                    gainers.append((ticker, percent_change))
            except KeyError:
                continue

        # Sort by the percentage change in descending order to get top gainers
        top_gainers = sorted(gainers, key=lambda x: x[1], reverse=True)[:3]
        return top_gainers

    def run(self, data):
        allocation_dict = {}
        current_time = datetime.now()

        # Market Open Logic
        if current_time.hour == 9 and current_time.minute <= 30:
            # Assuming data contains 'yesterday' data at this time
            yesterday_date = (current_time.date() - timedelta(days=1)).strftime('%Y-%m-%d')
            if 'ohlcv' in data and yesterday_date in data['ohlcv']:
                yesterday_data = data['ohlcv'][yesterday_date]
                top_gainers = self.select_top_gainers(yesterday_data)
                if top_gainers:
                    invest_amount = 1 / len(top_gainers)
                    for ticker, _ in top_gainers:
                        allocation_dict[ticker] = invest_amount
                    
        # Market Close Logic - assuming positions are cleared by the execution handler at market close
        # Hence, no explicit action required here for selling at close as per the given task's scope

        return TargetAllocation(allocation_dict)