from unittest.mock import patch
from src.main import ask, ask_choice, get_user_preferences, format_operation, main


def test_ask():
    with patch("builtins.input", return_value="   test input   ") as mock_input, \
         patch("builtins.print") as mock_print:
        result = ask("hello")
        assert result == "test input"
        mock_print.assert_called_once_with("Программа:\nhello")
        mock_input.assert_called_once_with("Пользователь: ")


def test_ask_choice_valid_on_first_try():
    with patch("src.main.ask", return_value="executed") as mock_ask:
        result = ask_choice("status", ["EXECUTED", "CANCELED"])
        assert result == "EXECUTED"
        mock_ask.assert_called_once_with("status")


def test_ask_choice_invalid_then_valid():
    with patch("src.main.ask", side_effect=["invalid", "canceled"]) as mock_ask, \
         patch("builtins.print") as mock_print:
        result = ask_choice("status", ["EXECUTED", "CANCELED"])
        assert result == "CANCELED"
        assert mock_ask.call_count == 2
        mock_print.assert_any_call("Программа:\nНекорректный ввод, возможные варианты:\nEXECUTED, CANCELED")


def test_ask_choice_invalid_with_default():
    with patch("src.main.ask", return_value="invalid") as mock_ask, \
         patch("builtins.print") as mock_print:
        result = ask_choice("status", ["EXECUTED", "CANCELED"], default="executed")
        assert result == "EXECUTED"
        mock_ask.assert_called_once_with("status")
        mock_print.assert_any_call("Программа:\nВыбрано значение по умолчанию: executed")


def test_ask_choice_invalid_with_error_message():
    with patch("src.main.ask", side_effect=["invalid", "canceled"]) as mock_ask, \
         patch("builtins.print") as mock_print:
        result = ask_choice("status", ["EXECUTED", "CANCELED"], error_message="Error: {}")
        assert result == "CANCELED"
        assert mock_ask.call_count == 2
        mock_print.assert_any_call("Программа:\nError: invalid")


def test_get_user_preferences():
    with patch("src.main.ask_choice", side_effect=["EXECUTED", "ДА", "1", "ДА", "ДА"]) as mock_choice, \
         patch("src.main.ask", return_value="test_keyword") as mock_ask:
        prefs = get_user_preferences()
        assert prefs == {
            "status": "EXECUTED",
            "sort_by_date": True,
            "sort_by_increase": False,
            "sort_by_currency": True,
            "sort_by_keyword": True,
            "keyword": "test_keyword",
            "file_type": "",
        }
        assert mock_choice.call_count == 5
        mock_ask.assert_called_once_with("Введите ключевое слово")


def test_get_user_preferences_no_keyword():
    with patch("src.main.ask_choice", side_effect=["CANCELED", "НЕТ", "2", "НЕТ", "НЕТ"]) as mock_choice, \
         patch("src.main.ask") as mock_ask:
        prefs = get_user_preferences()
        assert prefs == {
            "status": "CANCELED",
            "sort_by_date": False,
            "sort_by_increase": True,
            "sort_by_currency": False,
            "sort_by_keyword": False,
            "file_type": "",
        }
        assert mock_choice.call_count == 5
        mock_ask.assert_not_called()


def test_format_operation_with_from_field():
    op = {
        "date": "2019-08-26T10:50:58.294041",
        "description": "Перевод организации",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }
    expected = (
        "26.08.2019 Перевод организации\n"
        "Maestro 1596 83** **** 5199 -> Счет **9589\n"
        "Сумма: 31957.58 руб."
    )
    assert format_operation(op) == expected


def test_format_operation_without_from_field():
    op = {
        "date": "2019-07-03T18:35:29.512364",
        "description": "Открытие счета",
        "operationAmount": {"amount": "8000.00", "currency": {"name": "USD", "code": "USD"}},
        "to": "Счет 35383033474447895560"
    }
    expected = (
        "03.07.2019 Открытие счета\n"
        "Счет **5560\n"
        "Сумма: 8000 USD"
    )
    assert format_operation(op) == expected


@patch("src.main.ask_choice")
@patch("src.main.get_user_preferences")
@patch("src.main.load_operations")
def test_main_json_success(mock_load_ops, mock_get_prefs, mock_ask_choice, capsys):
    mock_ask_choice.return_value = "1"  # JSON
    mock_get_prefs.return_value = {
        "status": "EXECUTED",
        "sort_by_date": True,
        "sort_by_increase": False,
        "sort_by_currency": True,
        "sort_by_keyword": False,
        "file_type": "JSON"
    }
    mock_load_ops.return_value = [
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

    main()

    captured = capsys.readouterr()
    assert "Для обработки выбран JSON-файл" in captured.out
    assert "Всего банковских операций в выборке: 1" in captured.out
    assert "31957.58 руб." in captured.out


@patch("src.main.ask_choice")
@patch("src.main.get_user_preferences")
@patch("src.main.read_from_file")
def test_main_csv_success(mock_read_file, mock_get_prefs, mock_ask_choice, capsys):
    mock_ask_choice.return_value = "2"  # CSV
    mock_get_prefs.return_value = {
        "status": "EXECUTED",
        "sort_by_date": False,
        "sort_by_increase": False,
        "sort_by_currency": False,
        "sort_by_keyword": False,
        "file_type": "CSV"
    }
    mock_read_file.return_value = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        }
    ]

    main()

    captured = capsys.readouterr()
    assert "Для обработки выбран CSV-файл" in captured.out
    assert "Всего банковских операций в выборке: 1" in captured.out
    assert "USD" in captured.out


@patch("src.main.ask_choice")
@patch("src.main.get_user_preferences")
@patch("src.main.load_operations")
def test_main_file_not_found(mock_load_ops, mock_get_prefs, mock_ask_choice, capsys):
    mock_ask_choice.return_value = "1"
    mock_get_prefs.return_value = {
        "status": "EXECUTED",
        "sort_by_date": False,
        "sort_by_increase": False,
        "sort_by_currency": False,
        "sort_by_keyword": False,
        "file_type": "JSON"
    }
    mock_load_ops.return_value = []

    main()

    captured = capsys.readouterr()
    assert "Ошибка: Файл не найден!" in captured.out


@patch("src.main.ask_choice")
@patch("src.main.get_user_preferences")
@patch("src.main.load_operations")
def test_main_no_transactions_match(mock_load_ops, mock_get_prefs, mock_ask_choice, capsys):
    mock_ask_choice.return_value = "1"
    mock_get_prefs.return_value = {
        "status": "CANCELED",
        "sort_by_date": False,
        "sort_by_increase": False,
        "sort_by_currency": False,
        "sort_by_keyword": False,
        "file_type": "JSON"
    }
    mock_load_ops.return_value = [
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

    main()

    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out
