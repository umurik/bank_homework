import os
from unittest.mock import patch

import pytest
from dotenv import load_dotenv

from src.external_api import convert_transaction

load_dotenv()


@patch("src.external_api.requests.request")
def test_convert_transaction(mock_request, transactions_dict_usd, transactions_dict_rub):
    mock_response = mock_request.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 760654.06}
    assert convert_transaction(transactions_dict_usd[0]) == 760654.06
    mock_request.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": os.getenv("CURRENCY_API")},
        params={"to": "RUB", "from": "USD", "amount": "9824.07"},
    )
    assert convert_transaction(transactions_dict_rub[0]) == 43318.34


@patch("src.external_api.requests.request")
def test_error_convert_transaction(mock_request, transactions_dict_usd):
    mock_response = mock_request.return_value
    mock_response.status_code = 400
    with pytest.raises(ValueError) as exc_info:
        convert_transaction(transactions_dict_usd[0])
    assert str(exc_info.value) == "Error while getting response: 400"
    transaction_bad = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "р.", "code": "BYN"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    with pytest.raises(ValueError) as exc_info:
        convert_transaction(transaction_bad)
    assert str(exc_info.value) == "Except USD, RUB, EUR"
