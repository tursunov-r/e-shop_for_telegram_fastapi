import requests
import time
from requests.exceptions import RequestException, Timeout, ConnectionError
from typing import Optional

from fastapi import HTTPException

from src.core.settings import settings

API_KEY = settings.exchangerate_api_com_key


class ExchangeClient:
    def __init__(
        self,
        base_url: str = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest",
    ):
        self.base_url = base_url
        self.timeout = 5
        self.max_retries = 3

    def get_exchange_rate(self, base: str, target: str) -> Optional[float]:
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    f"{self.base_url}/{base}", timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()

                if target in data.get("conversion_rates", {}):
                    return data["conversion_rates"][target]
                raise HTTPException(
                    status_code=404, detail=f"Currency {target} not found"
                )
            except Timeout:
                if attempt < self.max_retries - 1:
                    delay = attempt**2
                    print(
                        f"Timed out waiting for exchange rate, trying again in {delay} seconds"
                    )
                    time.sleep(delay)
                else:
                    print("Timed out...")
                    return None
            except ConnectionError as e:
                if attempt < self.max_retries - 1:
                    delay = attempt**2
                    print(
                        f"Connection error... try again in {delay} seconds..."
                    )
                    time.sleep(delay)
                else:
                    print("Connection error...")
                    return None
            except RequestException as e:
                print(f"Request exception {e}")
                return None
        return None

    def convert_price(
        self, price: float, from_currency: str, to_currency: str
    ) -> Optional[float]:
        if from_currency == to_currency:
            return price

        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate is None:
            return None
        return rate * price


exchange_client = ExchangeClient()
convert_price = exchange_client.convert_price(1, "USD", "RUB")
if convert_price:
    print(f"1000 USD = {convert_price} RUB")
else:
    print("Cannot convert price")
