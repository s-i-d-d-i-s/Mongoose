import os
import requests
import json
import time

class Cache:
    def __init__(self, cache_dir='cache', expiry_seconds=12*60*60):
        self.cache_dir = os.path.join(os.path.dirname(__file__),  cache_dir)
        self.expiry_seconds = expiry_seconds # 12 hours
        os.makedirs(self.cache_dir, exist_ok=True)

    def get(self, key):
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            if time.time() - os.path.getmtime(cache_file) < self.expiry_seconds:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            else:
                os.remove(cache_file)
        return None

    def set(self, key, value):
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_file, 'w') as f:
            json.dump(value, f)


class ForexHandler:
    def __init__(self):
        self.cookies = {
            'gid': 'ce683d85-649a-4ee4-9b11-71a0dbf5b66a',
            'gid': 'ce683d85-649a-4ee4-9b11-71a0dbf5b66a',
            'twCookieConsent': '%7B%22policyId%22%3A%222023-10-16%22%2C%22expiry%22%3A1765656280849%2C%22isEu%22%3Atrue%2C%22status%22%3A%22accepted%22%7D',
            'twCookieConsentGTM': 'true',
            '__adal_ca': 'so%3DGoogle%26me%3Dorganic%26ca%3D%28not%2520set%29%26co%3D%28not%2520set%29%26ke%3D%28not%2520set%29%26cg%3DOrganic',
            '_ga': 'GA1.1.1482666819.1749931482',
            'FPID': 'FPID2.2.3JHq12abKxUpa4o4OZZnD5JX7AmIFVbcF0bM%2B6kcfks%3D.1749931482',
            'appToken': 'dad99d7d8e52c2c8aaf9fda788d8acdc',
            '__cf_bm': 'ggowpzfFDrfFlLHDrxY3TfxTEWZDItsiNgPo1vu5Zs4-1757746842-1.0.1.1-O1VLIDyJc7eezT733FasoAOVd8E9y.qqR8cuNfTj5WlasaweZpFFuaUhedUuZdYeSo9Cd1E72YSw2Imon7_i_iCi7g.rdEVqL7Ma3lFp7YnkqGxJy4ms4OhAIlBIg4G9',
            '_gcl_au': '1.1.1642849803.1757746844',
            '__adal_ses': '*',
            '__adal_cw': '1757746853560',
            'FPLC': 'sY1Bm4fYceRaHZYTDlRHmz4070OD0EHHrU%2FFSz8KPK5mHuH0kdhtyS%2BAwKSRIcVtVY9HdvHOrpPrTbCWLAZCG%2Fxaf2tOV1IFZkhztRN1Frs9ydJZxgzKUGX6lNdZJQ%3D%3D',
            'FPAU': '1.1.1642849803.1757746844',
            'FPGSID': '1.1757746853.1757746853.G-MFT2R11DFX.mZ9b9lr8_Pi4NG8bZjYztw',
            '_fbp': 'fb.1.1757746854003.1064162333',
            'did_linejpbyw': 'vvqp7y9-vgrm-psan-jvx-w2eks0c3260l',
            '_ga_MFT2R11DFX': 'GS2.1.s1757746853$o2$g1$t1757746862$j51$l0$h1664979860',
            '_rdt_uuid': '1757746853895.7e436302-72fd-4f63-8948-db9e201c461c',
            '_tq_id.TV-7290902709-1.649b': '6f6f4c69d3b2ffa7.1749931482.0.1757746863..',
            '__adal_id': '6b4c6ddf-d24f-424b-b818-7fbe5d9cf650.1749931482.3.1757746863.1749932341.f6b177b3-f4b9-4e77-9449-22c6b51a412c',
            'mp_e605c449bdf99389fa3ba674d4f5d919_mixpanel': '%7B%22distinct_id%22%3A%22%24device%3A1c9350c2-d504-4ee3-b60c-acb16235e9aa%22%2C%22%24device_id%22%3A%221c9350c2-d504-4ee3-b60c-acb16235e9aa%22%2C%22%24search_engine%22%3A%22google%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%22www.google.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%22www.google.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%7D',
            '_tq_id.TV-7290902709-1.649b': 'qlmqefcstz6m389u.1757746854.0.1757746863..',
        }

        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'gb',
            'priority': 'u=1, i',
            'referer': 'https://wise.com/gb/currency-converter/usd-to-eur-rate/history',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'x-access-token': 'Tr4n5f3rw153',
        }

        self.cache = Cache()

        self.eur_to_usd = self.fetch_forex_rates('EUR', 'USD')

    def fetch_forex_rates(self, source, target):
        cached_data = self.cache.get(f"{source}_{target}")
        if cached_data:
            print("Using cached data.")
            return cached_data
        print("Fetching new data from Wise.")
        params = {
            'source': source,
            'target': target,
            'length': '5',
            'unit': 'year',
            'resolution': 'daily',
        }

        response = requests.get('https://wise.com/rates/details', params=params, cookies=self.cookies, headers=self.headers)
        data = json.loads(response.content)
        if 'data' not in data:
            raise ValueError("Unexpected response structure: 'data' key not found.")
        self.cache.set(f"{source}_{target}", data['data'])
        return data['data']
    
    # Returns the exchange rate data for the specified source and target currencies.
    # The date format is YYYY-MM-DD.
    def get_rate_on_date(self, source, target, date_string):
        if source == "EUR" and target == "USD":
            data = self.eur_to_usd
        else:
            raise ValueError(f"No exchange rate found for {source} to {target} on {date_string}")

        from datetime import datetime
        # Convert to a datetime object
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        timestamp = int(date_object.timestamp())*1000
        for rate in data:
            if rate['time'] >= timestamp:
                return rate['value']
        # Throw an error if no rate is found for the given date
        raise ValueError(f"No exchange rate found for {source} to {target} on {date_string}")
