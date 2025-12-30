# Проект домашнего задания для колледжа

## Описание:

Данный проект содержит модули, который способны скрывать номер карты или счета, а так же форматировать дату в формате DD.MM.YYYY. 
В процессе выполнения домашних заданий данный репозиторий будет пополняться. 

## Цель: 
Получить знания по использованию Python, Git и других технологий для дальнейшего развития в сфере IT.

## Установка: 
1. Скопируйте репозиторий себе на диск с помощью команды git clone https://github.com/umurik/bank_homework.git.
2. Установите все зависимости с помощью poetry install(если у вас нет poetry, установите его с помощью pip)

## Использование:

1. Включите нужный вам модуль(masks, processing, widget) в ваш python проект
2. Используйте необходимые функции
3. Profit!

## Тестирование

Проект покрыт unit-тестами с использованием pytest.

### Запуск тестов
```pytest```
### Запуск с покрытием кода
```
pytest --cov=src --cov-report=html
```
### Структура тестов

- `tests/test_masks.py` — тесты для функций маскирования карт и счетов
- `tests/test_processing.py` — тесты для функций фильтрации и сортировки
## Примеры:

### Masks:
```
from masks import get_mask_account, get_mask_card_number

print(f"Ваш счет: {get_mask_account('1234567891234')}")
print(f"Ваш номер карты: {get_mask_card_number('1234567891234567')}")

Вывод кода:
    Ваш счет: **1234
    Ваш номер карты: 1234 56** **** 4567
 
```
### Widget:

```
from widget import mask_account_card, get_date
print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 7000792289606361"))
print(get_date("2024-03-11T02:26:18.671407"))

Вывод кода:
    Visa Platinum 7000 79** **** 6361
    Счет **6361
    11.03.2024
```
### Processing:
```
from processing import sort_by_date, filter_by_state

dict_list = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

print(f"Executed: {filter_by_state(dict_list)}")
print(f"Canceled: {filter_by_state(dict_list, state="CANCELED")}")
print(f"Sorted by date(decreasing): {sort_by_date(dict_list)}")
print(f"Sorted by date(increasing): {sort_by_date(dict_list, sort_by_decreasing=False)}")

Вывод кода:
    Executed: [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    Canceled: [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    Sorted by date(decreasing): [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    Sorted by date(increasing): [{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}]
```

