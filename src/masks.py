import logging
import os

logger = logging.getLogger(__name__)
if not os.path.exists(os.path.join("..", "logs")):
    os.makedirs(os.path.join("..", "logs"))
file_handler = logging.FileHandler(os.path.join("..", "logs", "masks.log"))
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Getting card number and return masked card number"""
    logger.debug("Trying mask card number")
    if card_number is None:
        logger.error("Card number is None")
        raise ValueError("Wrong card number")
    if len(card_number) != 16 or not card_number.isdigit():
        logger.error(f"Card number length != 16 or not digit: {card_number}")
        raise ValueError("Wrong card number")
    temp = list(card_number)
    mask_start = 5
    mask_end = 12
    logger.debug("Replacing card numbers digits to *")
    for i in range(len(card_number)):
        if mask_start < i < mask_end:
            temp[i] = "*"
    masked_card_number = "".join(temp)
    blocks = list()
    logger.debug("Converting list to string")
    for i in range(0, len(card_number), 4):
        blocks.append(masked_card_number[i : i + 4])
    formatted_card_number = " ".join(blocks)
    logger.debug("Card number encrypted successfully")
    return formatted_card_number


def get_mask_account(bank_account: str) -> str:
    """Getting bank account and return masked bank account"""
    if bank_account is None:
        logger.error("Bank account is None")
        raise ValueError("Wrong bank account")
    if bank_account.isdigit() and len(bank_account) >= 4:
        logger.debug("Replacing digits to *")
        formatted_bank_account = "**" + bank_account[-4:]
        logger.debug("Bank account encrypted successfully")
        return formatted_bank_account
    else:
        logger.error("Bank account is not digit or length < 4")
        raise ValueError("Wrong bank account")
