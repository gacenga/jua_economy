import requests

class EconomicDataFetcher:
    BASE_URL = "https://api.worldbank.org/v2/country/"

    def __init__(self, country_code="KEN", start_year=2000, end_year=2023):
        self.country_code = country_code
        self.start_year = start_year
        self.end_year = end_year

    def fetch_data(self, indicator, processor):
        url = f"{self.BASE_URL}{self.country_code}/indicator/{indicator}?date={self.start_year}:{self.end_year}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                return processor(data[1])
            else:
                print(f"No data found for indicator: {indicator}")
                return []
        else:
            response.raise_for_status()

    def process_data(self, data, value_key):
        processed_data = []
        for item in data:
            year = item.get('date')
            value = item.get('value')
            if year and value is not None:
                processed_data.append({
                    "year": year,
                    value_key: value
                })
        return processed_data

    def fetch_gdp_data(self):
        return self.fetch_data('NY.GDP.MKTP.CD', lambda data: self.process_data(data, 'gdp'))

    def fetch_trade_balance_data(self):
        return self.fetch_data('NE.EXP.GNFS.CD', lambda data: self.process_data(data, 'trade_balance'))

    def fetch_unemployment_data(self):
        return self.fetch_data('SL.UEM.TOTL.ZS', lambda data: self.process_data(data, 'unemployment_rate'))

    def fetch_govt_spending_data(self):
        return self.fetch_data('GC.XPN.TOTL.CD', lambda data: self.process_data(data, 'govt_spending'))

    def fetch_inflation_data(self):
        return self.fetch_data('FP.CPI.TOTL', lambda data: self.process_data(data, 'inflation_rate'))

    def fetch_interest_rates_data(self):
        return self.fetch_data('FR.INR.RINR', lambda data: self.process_data(data, 'interest_rate'))

    def fetch_exchange_rates_data(self):
        return self.fetch_data('PA.NUS.FCRF', lambda data: self.process_data(data, 'exchange_rate'))
