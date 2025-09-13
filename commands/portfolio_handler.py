class PortfolioHandler:
    def __init__(self, currency="USD"):
        # Stores portfolio as {ticker: {'shares': float, 'avg_price': float}}
        self.portfolio = {}
        self.currency = currency

    def buy(self, ticker, shares, price_per_share):
        """
        Add shares to the portfolio and update the average price.
        """
        if ticker not in self.portfolio:
            self.portfolio[ticker] = {'shares': 0.0, 'avg_price': 0.0}
        current = self.portfolio[ticker]
        total_cost = current['avg_price'] * current['shares'] + price_per_share * shares
        current['shares'] += shares
        # Round shares to avoid floating point issues
        current['shares'] = round(current['shares'], 8)
        if current['shares'] > 0:
            current['avg_price'] = total_cost / current['shares']
        else:
            current['avg_price'] = 0.0

    def sell(self, ticker, shares, price_per_share):
        """
        Remove shares from the portfolio and return the realized gain/loss.
        Returns None if not enough shares.
        """
        if ticker not in self.portfolio or self.portfolio[ticker]['shares'] < shares:
            raise ValueError(f"Not enough shares to sell for {ticker}. Available: {self.portfolio.get(ticker, {}).get('shares', 0)} shares. Requested: {shares} shares.")
        current = self.portfolio[ticker]
        gain = (price_per_share - current['avg_price']) * shares
        current['shares'] -= shares
        # Round shares to avoid floating point issues
        current['shares'] = round(current['shares'], 8)
        if current['shares'] == 0:
            # Remove ticker from portfolio if no shares left
            del self.portfolio[ticker]
        return gain

    def get_position(self, ticker):
        """
        Returns the current position for a ticker as a dict, or None if not held.
        """
        return self.portfolio.get(ticker)

