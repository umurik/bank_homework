def get_mask_card_number(card_number: str) -> str:
    """Getting card number and return masked card number"""
    if len(card_number) != 16:
        raise ValueError("Wrong card number")
    temp = list(card_number)
    mask_start = 5
    mask_end = 12
    for i in range(len(card_number)):
        if mask_start < i < mask_end:
            temp[i] = "*"
    masked_card_number = "".join(temp)
    blocks = list()
    for i in range(0, len(card_number), 4):
        blocks.append(masked_card_number[i : i + 4])
    formatted_card_number = " ".join(blocks)
    return formatted_card_number


def get_mask_account(bank_account: str) -> str:
    """Getting bank account and return masked bank account"""
    if bank_account.isdigit() and len(bank_account) >= 4:
        formatted_bank_account = "**" + bank_account[-4:]
        return formatted_bank_account
    else:
        raise ValueError("Wrong bank account")
