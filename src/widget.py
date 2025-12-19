import re
from masks import get_mask_account
from masks import get_mask_card_number



def mask_account_card(bank_account: str) -> str:
    """Getting account with card number or bank account and returning account with masked numbers"""
    bank_digits = "".join(re.findall(r"\d+", bank_account))
    bank_chars = "".join(re.findall(r"\D", bank_account))
    if bank_digits == "" or not bank_chars.strip():
        raise ValueError("Wrong bank account or card number")
    if bank_chars != "Счет":
        return f"{bank_chars + get_mask_card_number(bank_digits)}"
    else:
        return f"{bank_chars + get_mask_account(bank_digits)}"


