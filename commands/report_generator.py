import os
import json
from commands.forex_handler import ForexHandler

class PortfolioHandler:
    def __init__(self):
        # Stores portfolio as {ticker: {'shares': float, 'avg_price': float}}
        self.portfolio = {}

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

class ReportGenerator:
    def __init__(self, target_file, currency):
        self.forex = ForexHandler()
        self.data = {}
        self.target_file = target_file
        self.currency = currency


        normalized_data = os.listdir('normalized')
        print("Generating report from normalized data files:")
        for data in normalized_data:
            print(f" - {data}")
            self.data = json.load(open(os.path.join('normalized', data)))
        os.makedirs('report', exist_ok=True)
        
    def __get_forex_adjusted_amount(self, source, target, date, amount):
        """ Converts an amount from source currency to target currency on a specific date.
        Uses the ForexHandler to get the exchange rate for the given date.
        """
        if source == target:
            return amount
        return self.forex.get_rate_on_date(source, target, date) * amount
    
    def generate_report(self):
        report = {
            'dividends': 0.0,
            'capital_gains': 0.0,
            'interest': 0.0,
        }
        report_log = ""

        # Compute Dividends
        report_log += "Dividends Report:\n"
        for data in self.data['dividends']:
            forex_adjusted_amount = self.__get_forex_adjusted_amount(data['currency'], self.currency, data['date'], data['amount'])
            report_log += f"{data['ticker']} Dividend: {data['amount']} {data['currency']} on {data['date']} converted to {forex_adjusted_amount:.2f} {self.currency}\n"
            report['dividends'] += forex_adjusted_amount
        
        # Compute Interest
        report_log += "Interest Report:\n"
        for data in self.data['interest']:
            forex_adjusted_amount = self.__get_forex_adjusted_amount(data['currency'], self.currency, data['date'], data['amount'])
            report_log += f"Interest Paid: {data['amount']} {data['currency']} on {data['date']} converted to {forex_adjusted_amount:.2f} {self.currency}\n"
            report['interest'] += forex_adjusted_amount

        # Compute Capital Gains
        portfolio = PortfolioHandler()
        report_log += "Capital Gains Report:\n"
        for data in self.data['orders']:
            forex_adjusted_price = self.__get_forex_adjusted_amount(data['currency'], self.currency, data['date'], data['price'])
            if data['type'] == 'BUY':
                portfolio.buy(data['ticker'], data['units'], forex_adjusted_price)
                report_log += f"Bought {data['units']} shares of {data['ticker']} at {data['price']} {data['currency']} converted to {forex_adjusted_price} {self.currency} on {data['date']}\n"
            elif data['type'] == 'SELL':
                gain = portfolio.sell(data['ticker'], data['units'], forex_adjusted_price)
                report_log += f"Sold {data['units']} shares of {data['ticker']} at {data['price']} {data['currency']} converted to {forex_adjusted_price} {self.currency} on {data['date']} with gain/loss of {gain:.2f} {self.currency}\n"
                report['capital_gains'] += gain

        with open(f'report/{self.target_file}.json', 'w') as f:
            f.write(json.dumps(report))
        with open(f'report/{self.target_file}.txt', 'w') as f:
            f.write(report_log)