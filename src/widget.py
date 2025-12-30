import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(bank_account: str) -> str:
    """Getting account with card number or bank account and returning account with masked numbers"""
    if bank_account is None:
        raise ValueError("Wrong bank account or card number")
    bank_digits = "".join(re.findall(r"\d+", bank_account))
    bank_chars = "".join(re.findall(r"\D", bank_account))
    if bank_digits == "" or not bank_chars.strip():
        raise ValueError("Wrong bank account or card number")
    if bank_chars.strip() != "Счет":
        return f"{bank_chars + get_mask_card_number(bank_digits)}"
    else:
        return f"{bank_chars + get_mask_account(bank_digits)}"


def get_date(unformatted_date: str) -> str:
    """Getting unformatted date and return date in format 'DD.MM.YYYY'"""
    if unformatted_date is None:
        raise ValueError("Can't found date in format YYYY-MM-DD")
    date = "".join(re.findall(r"\d{4}-\d{2}-\d{2}", unformatted_date))
    if date == "":
        raise ValueError("Can't found date in format YYYY-MM-DD")
    formatted_date = re.sub(r"(\d{4}).(\d{2}).(\d{2})", r"\3.\2.\1", date)
    return formatted_date
