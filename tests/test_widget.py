import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "bank_account, masked_bank_account",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ],
)
def test_mask_account_card(bank_account: str, masked_bank_account: str):
    assert mask_account_card(bank_account) == masked_bank_account


@pytest.mark.parametrize("wrong_bank_acc", ["123421", "APS{LDolf", "", "121", None])
def test_mask_account_car_bad(wrong_bank_acc: str):
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(wrong_bank_acc)
    assert str(exc_info.value) == "Wrong bank account or card number"


@pytest.mark.parametrize(
    "date, form_date", [("2024-03-11T02:26:18.671407", "11.03.2024"), ("aoskmdp2025-12-31asdfas", "31.12.2025")]
)
def test_get_date(date: str, form_date: str):
    assert get_date(date) == form_date


@pytest.mark.parametrize("bad_date", ["20s4-03-11T02:26:18.671407", "aoskmdp2025a12-31asdfas", "asd", "", None])
def test_get_date_errors(bad_date: str):
    with pytest.raises(ValueError) as exc_info:
        get_date(bad_date)
    assert str(exc_info.value) == "Can't found date in format YYYY-MM-DD"
