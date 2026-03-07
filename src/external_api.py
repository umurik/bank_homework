import os

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_transaction(transaction: dict) -> float:
    """Function for converting currency from EUR, USD to RUB.

    Args:
        transaction: Dictionary with info about transactions.

    Returns:
        Float."""

    currency = transaction["operationAmount"]
    if currency["currency"]["code"] in ("USD", "EUR"):
        url = "https://api.apilayer.com/exchangerates_data/convert"
        headers = {"apikey": os.getenv("CURRENCY_API")}
        payload = {"to": "RUB", "from": currency["currency"]["code"], "amount": currency["amount"]}
        response = requests.request("GET", url, headers=headers, params=payload)
        if response.status_code == 200:
            return float(response.json()["result"])
        else:
            raise ValueError(f"Error while getting response: {response.status_code}")
    elif currency["currency"]["code"] == "RUB":
        return float(currency["amount"])
    else:
        raise ValueError("Except USD, RUB, EUR")
