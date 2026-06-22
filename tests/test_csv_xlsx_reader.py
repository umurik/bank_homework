import pandas as pd
from unittest.mock import patch, MagicMock
from src.csv_xlsx_reader import read_from_file


def test_read_from_file_csv_success():
    # Mocking pandas.read_csv to return a DataFrame
    mock_df = pd.DataFrame({
        "id": [650703],
        "state": ["EXECUTED"],
        "date": ["2023-09-05T11:30:32Z"],
        "amount": [16210.0],
        "currency_name": ["Sol"],
        "currency_code": ["PEN"],
        "from": ["Счет 58803664561298323391"],
        "to": ["Счет 39745660563456619397"],
        "description": ["Перевод организации"]
    })
    
    with patch("pandas.read_csv", return_value=mock_df):
        result = read_from_file("dummy.csv")
        assert len(result) == 1
        assert result[0]["id"] == 650703
        assert result[0]["operationAmount"]["amount"] == "16210.0"


def test_read_from_file_xlsx_success():
    # Mocking pandas.read_excel
    mock_df = pd.DataFrame({
        "id": [123],
        "state": ["EXECUTED"],
        "date": ["2023-01-01"],
        "amount": [100.0],
        "currency_name": ["руб."],
        "currency_code": ["RUB"],
        "from": [""],
        "to": ["Счет 123"],
        "description": ["Test"]
    })
    
    with patch("pandas.read_excel", return_value=mock_df):
        result = read_from_file("dummy.xlsx")
        assert len(result) == 1
        assert result[0]["id"] == 123


def test_read_from_file_unsupported_type():
    try:
        read_from_file("dummy.txt")
    except ValueError as e:
        assert str(e) == "This type of file doesn't support"


def test_read_from_file_not_found():
    # pandas raises FileNotFoundError if file doesn't exist
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        result = read_from_file("missing.csv")
        assert result == []
