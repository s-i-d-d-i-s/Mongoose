import pandas as pd
from commands import portfolio_handler
from datetime import datetime


class Trading212Handler:
    def __init__(self, data, currency, forex_handler):
        self.data = data
        self.currency = currency
        self.forex_handler = forex_handler
        self.normalized_data = {
            'interest': [],
            'orders' : [],
            'dividends' : [],
        }
        

    def __get_forex_adjusted_amount(self, source, target, date, amount):
        """ Converts an amount from source currency to target currency on a specific date.
        Uses the ForexHandler to get the exchange rate for the given date.
        """
        if source == target:
            return amount
        # Create a ForexHandler instance for the source and target currencies
        return self.forex_handler.get_rate_on_date(source, target, date) * amount

    def __get_formatted_date(self, timestamp):
        """
        Converts a timestamp string to a formatted date string.
        Handles both formats with and without fractional seconds.
        """
        try:
            dt_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            dt_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt_object.strftime("%Y-%m-%d %I:%M %p")

    
   
    # Computes the interest on cash holdings in the portfolio.
    def compute_interest(self):
        data = self.data[self.data['Action'].isin(['Interest on cash'])]
        for index, row in data.iterrows():
            total = row['Total']
            currency = row['Currency (Total)']
            timestamp = row['Time']
            formatted_date = self.__get_formatted_date(timestamp)
            amount = self.__get_forex_adjusted_amount(currency, self.currency, formatted_date, total)
            self.normalized_data['interest'].append([formatted_date, amount])
    
    # def compute_stock_capital_gains(self, target_currency):
    #     # Filter relevant actions
    #     data = self.data[self.data['Action'].isin(['Market buy', 'Market sell', 'Limit buy', 'Limit sell'])]
    #     # Initialize tracking dictionaries

    #     for index, row in data.iterrows():
    #         action = row['Action']
    #         currency = row['Currency (Price / share)']
    #         if currency != target_currency:
    #             continue  # Skip if the currency is not the target currency
    #         ticker = row['Ticker']
    #         shares = row['No. of shares']
    #         price_per_share = row['Price / share']
    #         timestamp = row['Time']
    #         formatted_date = self.__get_formatted_date(timestamp)

    #         if action in ['Market buy', 'Limit buy']:
    #             self.normalized_data['orders'].append([formatted_date, 'BUY', shares, ticker, price_per_share])
    #             portfolio.buy(ticker, shares, price_per_share)
    #         elif action in ['Market sell', 'Limit sell']:
    #             # Sell and calculate capital gains in the transaction currency
    #             gains = portfolio.sell(ticker, shares, price_per_share)
    #             # Convert to target_currency if needed
    #             amount = self.__get_forex_adjusted_amount(currency, self.currency, formatted_date, gains)
    #             capital_gains += amount
    #             self.__log_transaction(action, shares, ticker, price_per_share, currency, formatted_date, gains, target_currency, amount)
    #             # Add to pnl dictionary in target currency
    #             self.__add_to_pnl_dictionary(formatted_date, amount)
    
    # Computes the total dividends received in the portfolio.
    def compute_total_dividends(self, target_currency):
        data = self.data[self.data['Action'] == 'Dividend (Dividend)']
        for index, row in data.iterrows():
            currency = row['Currency (Total)']
            if currency != target_currency:
                continue  # Skip if the currency is not the target currency
            total = row['Total']
            timestamp = row['Time']
            formatted_date = self.__get_formatted_date(timestamp)
            amount = self.__get_forex_adjusted_amount(currency, target_currency, formatted_date, total)
            self.normalized_data['dividends'].append([formatted_date, amount])


    def get_normalized_data(self):
        """
        Fetches the total profit, dividends, interest and loss for entire portfolio.
        """
        if self.data is None:
            return None
        self.compute_interest()
        self.compute_total_dividends("EUR")
        self.compute_total_dividends("USD")

        # self.compute_stock_capital_gains("EUR")
        # self.compute_stock_capital_gains("USD")
        
        return self.normalized_data

