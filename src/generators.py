from typing import Generator, Iterator


def filter_by_currency(dict_list: list, currency: str) -> Iterator[dict]:
    """Function for filtering by currency, getting dictionary list and return Iterator"""
    if not isinstance(currency, str):
        raise TypeError(f"Expected str, received {type(currency)}")
    return (
        filtered_dict
        for filtered_dict in dict_list
        if filtered_dict.get("operationAmount", {}).get("currency", {}).get("name", "").upper() == currency.upper()
        or filtered_dict.get("operationAmount", {}).get("currency", {}).get("code", "").upper() == currency.upper()
    )


def transaction_descriptions(dict_list: list) -> Iterator[str]:
    """Func for transaction description, getting dictionary list and return Iterator[str]"""
    for transaction in dict_list:
        yield transaction.get("description", "Без описания")


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Func for card number generation, getting range for generation, return Generator[str]"""
    if not isinstance(start, int) or not isinstance(stop, int):
        raise TypeError(f"Expected int, received {type(start)}, {type(stop)}")
    if start > stop:
        raise ValueError("Card number start > Card number end")
    card_size = 16
    for card_number_int in range(start, stop + 1):
        card_number = str(card_number_int).zfill(card_size)
        blocks = [card_number[i : i + 4] for i in range(0, len(card_number), 4)]
        formatted_card_number = " ".join(blocks)
        yield formatted_card_number
