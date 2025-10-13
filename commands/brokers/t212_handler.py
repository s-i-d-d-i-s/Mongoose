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

    def fetch_interest(self):
        data = self.data[self.data['Action'].isin(['Interest on cash'])]
        for _, row in data.iterrows():
            total = row['Total']
            currency = row['Currency (Total)']
            timestamp = row['Time']
            formatted_date = self.__get_formatted_date(timestamp)
            self.normalized_data['interest'].append({'date': formatted_date, 'amount': total, 'currency': currency})
    
    def fetch_orders(self):
        # Filter relevant actions
        data = self.data[self.data['Action'].isin(['Market buy', 'Market sell', 'Limit buy', 'Limit sell'])]

        for _, row in data.iterrows():
            action = row['Action']
            currency = row['Currency (Price / share)']
            ticker = row['Ticker']
            shares = row['No. of shares']
            price_per_share = row['Price / share']
            timestamp = row['Time']
            formatted_date = self.__get_formatted_date(timestamp)

            if action in ['Market buy', 'Limit buy']:
                self.normalized_data['orders'].append({ 'ticker': ticker, 'date': formatted_date, 'type': 'BUY', 'currency': currency, 'units': shares, 'ticker': ticker, 'price': price_per_share})
            elif action in ['Market sell', 'Limit sell']:
                self.normalized_data['orders'].append({ 'ticker': ticker, 'date': formatted_date, 'type': 'SELL', 'currency': currency, 'units': shares, 'ticker': ticker, 'price': price_per_share})
    
    #  Fetch all dividends received in the portfolio.
    def fetch_dividends(self):
        data = self.data[self.data['Action'] == 'Dividend (Dividend)']
        for _, row in data.iterrows():
            currency = row['Currency (Total)']
            total = row['Total']
            ticker = row['Ticker']
            timestamp = row['Time']
            formatted_date = self.__get_formatted_date(timestamp)
            self.normalized_data['dividends'].append({'ticker': ticker, 'date': formatted_date, 'amount': total, 'currency': currency})


    def get_normalized_data(self):
        """
        Fetches the total profit, dividends, interest and loss for entire portfolio.
        """
        if self.data is None:
            return None
        self.fetch_interest()
        self.fetch_dividends()
        self.fetch_orders()
        
        return self.normalized_data

