import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_card_number_generator():
    temp = card_number_generator(1, 3)
    expected_list = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
    for expected in expected_list:
        assert next(temp) == expected

    with pytest.raises(StopIteration) as exc_info:
        next(temp)
    assert str(exc_info.value) == ""

    with pytest.raises(ValueError) as exc_info:
        next(card_number_generator(5, 1))
    assert str(exc_info.value) == "Card number start > Card number end"

    assert next(card_number_generator(1, 1)) == "0000 0000 0000 0001"


def test_card_number_generator_errors():
    with pytest.raises(TypeError) as exc_info:
        next(card_number_generator("asdasda", "asd"))
    assert str(exc_info.value) == f"Expected int, received {type("")}, {type("")}"


def test_transaction_descriptions(transactions_dict_list):
    temp = transaction_descriptions(transactions_dict_list)
    expected_values = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    for expected in expected_values:
        assert next(temp) == expected
    with pytest.raises(StopIteration) as exc_info:
        next(temp)
    assert str(exc_info.value) == ""


def test_transaction_descriptions_empty_list():
    temp = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(temp)


def test_filter_by_currency_no_matches(transactions_dict_list):
    temp = filter_by_currency(transactions_dict_list, "CHF")
    with pytest.raises(StopIteration):
        next(temp)


def test_filter_by_currency_usd_rub(transactions_dict_list, transactions_dict_usd, transactions_dict_rub):
    temp = filter_by_currency(transactions_dict_list, "USD")
    for expected in transactions_dict_usd:
        assert next(temp) == expected

    with pytest.raises(StopIteration) as exc_info:
        next(temp)
    assert str(exc_info.value) == ""

    temp = filter_by_currency(transactions_dict_list, "RuB")
    for expected in transactions_dict_rub:
        assert next(temp) == expected


def test_filter_by_currency_invalid_currency_type(transactions_dict_list):
    with pytest.raises(TypeError) as exc_info:
        filter_by_currency(transactions_dict_list, 122331)
    assert str(exc_info.value) == f"Expected str, received {type(122331)}"
