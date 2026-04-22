import requests
import time

from requests.exceptions import RequestException, Timeout, ConnectionError
from typing import Optional

from src.core.settings import settings

EXCHANGERATE_API_COM_KEY = settings.exchangerate_api_com_key
EXCHANGERATES_API_IO_KEY = settings.exchangerates_api_io_key
OPENEXCHANGERATES_ORG_KEY = settings.openexchangerates_org_key


class MultyExchangeClient:
    def __init__(self):
        self.exchangerate_api_com_url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_COM_KEY}/latest"
        self.exchangerates_api_io_url = f"https://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGERATES_API_IO_KEY}"
        self.openexchangerates_org_url = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGERATES_ORG_KEY}"
        self.urls = [
            self.exchangerate_api_com_url,
            self.exchangerates_api_io_url,
            self.openexchangerates_org_url,
        ]
        self.timeout = 5
        self.max_retries = 3

    def get_exchange_rate(
        self, base_currency: str, target_currency: str
    ) -> Optional[float]:
        base_currency = base_currency.upper()
        target_currency = target_currency.upper()
        for url in self.urls:
            for attempt in range(self.max_retries):
                try:
                    if url == self.exchangerate_api_com_url:
                        response = requests.get(
                            f"{url}/{base_currency}", timeout=self.timeout
                        )

                    elif url == self.exchangerates_api_io_url:
                        response = requests.get(url, timeout=self.timeout)
                    else:
                        response = requests.get(url, timeout=self.timeout)
                    response.raise_for_status()
                    data = response.json()
                    # структура json отличается, по этому проверяем валюту через or под каждую структуру
                    if target_currency in data.get(
                        "conversion_rates", {}
                    ) or target_currency in data.get("rates", {}):
                        if url == self.exchangerate_api_com_url:
                            return data["conversion_rates"][target_currency]
                        elif url == self.exchangerates_api_io_url:
                            # логика такая, так как нет возможности выбрать конвертируемую валюту с api
                            # api возвращает только евро и словарь с валютами к евро
                            # конвертируем base_currency в EUR и только потом в Target
                            base = data["rates"][base_currency]
                            target = data["rates"][target_currency]
                            convert = 1 / base * target
                            return convert
                        elif url == self.openexchangerates_org_url:
                            return data["rates"][target_currency]
                    else:
                        print("Currency not found")
                except Timeout:
                    if attempt < self.max_retries - 1:
                        delay = attempt**2
                        print(f"Timeout, trying again in {delay} seconds")
                        time.sleep(delay)
                    else:
                        print(f"Timeout error")
                except ConnectionError:
                    if attempt < self.max_retries - 1:
                        delay = attempt**2
                        print(
                            f"Connection error, trying again in {delay} seconds"
                        )
                        time.sleep(delay)
                    else:
                        print(f"Connection error")
                except RequestException as e:
                    print(f"Request error: {e}")
        return None

    def __convert_price(
        self, price: float, from_currency: str, to_currency: str
    ) -> Optional[float]:
        if from_currency == to_currency:
            return price

        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate is None:
            return None
        return rate * price

    def get_response(
        self, price: float, from_currency: str, to_currency: str
    ) -> str:
        result = self.__convert_price(price, from_currency, to_currency)
        if result:
            return f"{price} {from_currency} = {result} {to_currency}"
        else:
            return "Cannot convert price"
