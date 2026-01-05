import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def dict_list():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


sorted_decreasing = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
]

sorted_increasing = [
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
]

filtered_by_executed = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
]

filtered_by_canceled = [
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


@pytest.mark.parametrize(
    "result, arg",
    [
        (filtered_by_executed, "EXECUTED"),
        (filtered_by_canceled, "CANCELED"),
        (filtered_by_canceled, "canCELED"),
        (filtered_by_executed, "executed"),
    ],
)
def test_filter_by_state(dict_list, result, arg):
    assert filter_by_state(dict_list, arg) == result


def test_filter_by_state_without_arg(dict_list):
    assert filter_by_state(dict_list) == filtered_by_executed


@pytest.mark.parametrize("dict_list_bad, arg", [("", "executed"), (9, "canceled"), ([], "")])
def test_filter_by_state_errors(dict_list_bad, arg):
    with pytest.raises(ValueError) as exc_info:
        filter_by_state(dict_list_bad, arg)
    assert str(exc_info.value) == "Wrong dictionary list or statement value"


def test_sort_by_date(dict_list):
    assert sort_by_date(dict_list) == sorted_decreasing


def test_sort_by_date_increasing(dict_list):
    assert sort_by_date(dict_list, False) == sorted_increasing


@pytest.mark.parametrize("dict_list_bad, arg", [("", True), ("asd", False), ([], ""), (None, None)])
def test_sort_by_date_errors(dict_list_bad, arg):
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(dict_list_bad, arg)
    assert str(exc_info.value) == "Wrong dictionary list or boolean value"
