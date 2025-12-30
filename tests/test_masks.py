import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, card_masked_number",
    [("7000792289606361", "7000 79** **** 6361"), ("1596837868705199", "1596 83** **** 5199")],
)
def test_get_mask_card_number(card_number: str, card_masked_number: str):
    assert get_mask_card_number(card_number) == card_masked_number


@pytest.mark.parametrize(
    "bank_account, bank_masked_account", [("64686473678894779589", "**9589"), ("35383033474447895560", "**5560")]
)
def test_get_mask_account(bank_account: str, bank_masked_account: str):
    assert get_mask_account(bank_account) == bank_masked_account


@pytest.mark.parametrize(
    "bad_card_number",
    [
        "1234",
        "-1232",
        "",
        "1234sjidof6789012345",
        "1234 5678 9012 3456",
        "asdfasdfasdfasdf",
        "123456789123456789",
        None,
    ],
)
def test_get_mask_card_number_errors(bad_card_number: str):
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(bad_card_number)
    assert str(exc_info.value) == "Wrong card number"


@pytest.mark.parametrize("bad_bank_account", ["", "-1", "aasdsdd", "123", "1", None])
def test_get_mask_account_errors(bad_bank_account: str):
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(bad_bank_account)
    assert str(exc_info.value) == "Wrong bank account"
