import json
from unittest.mock import patch, mock_open
from src.utils import load_operations


def test_load_operations_success():
    mock_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        }
    ]
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        assert load_operations("dummy.json") == mock_data


def test_load_operations_empty_path():
    assert load_operations("") == []
    assert load_operations(None) == []


def test_load_operations_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("src.utils.logger.exception") as mock_log:
            try:
                load_operations("dummy.json")
            except Exception:
                pass
            mock_log.assert_called_once()


def test_load_operations_not_a_list():
    with patch("builtins.open", mock_open(read_data=json.dumps({"not": "a list"}))):
        with patch("src.utils.logger.exception") as mock_log:
            try:
                load_operations("dummy.json")
            except Exception:
                pass
            mock_log.assert_called_once()
