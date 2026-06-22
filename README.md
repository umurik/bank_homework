# Проект домашнего задания для колледжа

## Описание:

Данный проект содержит модули для работы с банковскими транзакциями. Он позволяет скрывать номера карт и счетов, форматировать даты, фильтровать и сортировать операции, а также работать с различными форматами файлов (JSON, CSV, XLSX).
В проекте реализован интерактивный консольный интерфейс для удобного взаимодействия с пользователем.

### upd:

- Был добавлен основной модуль `main.py` с интерактивным интерфейсом.
- Был добавлен декоратор для логирования функций.
- Были добавлены модули для чтения JSON транзакций и перевода курса валют через API.
- Был добавлен модуль для чтения операций из файлов CSV и XLSX с использованием `pandas`.
- Все модули покрыты тестами на 80%+.

## Цель: 
Получить знания по использованию Python, Git и других технологий для дальнейшего развития в сфере IT.

## Установка: 
1. Скопируйте репозиторий себе на диск с помощью команды `git clone https://github.com/umurik/bank_homework.git`.
2. Установите все зависимости с помощью `poetry install` (если у вас нет poetry, установите его с помощью pip).

## Использование:

1. Запустите основной модуль программы: `python src/main.py`
2. Следуйте инструкциям в консоли для выбора файла и настройки фильтрации.
3. Или используйте отдельные модули в своем коде: `masks`, `processing`, `widget`, `generators`, `decorators`, `utils`, `external_api`, `csv_xlsx_reader`.

## Тестирование

Проект покрыт unit-тестами с использованием pytest.

### Запуск тестов
```bash
pytest
```
### Запуск с покрытием кода
```bash
pytest --cov=src --cov-report=html
```
### Структура тестов

- `tests/test_main.py` — тесты для основного интерфейса и логики приложения
- `tests/test_masks.py` — тесты для функций маскирования карт и счетов
- `tests/test_processing.py` — тесты для функций фильтрации и сортировки
- `tests/test_widget.py` — тесты для функций маскирования и форматирования даты
- `tests/test_generators.py` — тесты для функций-генераторов
- `tests/test_decorators.py` — тесты для декораторов
- `tests/test_utils.py` — тесты для утилит (загрузка JSON)
- `tests/test_external_api.py` — тесты для модулей конвертации валют
- `tests/test_csv_xlsx_reader.py` — тесты для чтения CSV и XLSX файлов

## Примеры:

### Main (Интерактивный интерфейс):
```bash
python src/main.py
```
```
Программа:
Привет! Добро пожаловать в программу работы с банковскими транзакциями.
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
Выберите необходимый пункт меню: 1
...
```

### Masks:
```python
from src.masks import get_mask_account, get_mask_card_number

print(f"Ваш счет: {get_mask_account('1234567891234')}")
print(f"Ваш номер карты: {get_mask_card_number('1234567891234567')}")
```
```
Вывод кода:
    Ваш счет: **1234
    Ваш номер карты: 1234 56** **** 4567
```

### External API (Конвертация):
```python
from src.external_api import convert_transaction

transaction = {
    "operationAmount": {"amount": "100", "currency": {"code": "USD"}}
}
print(f"Сумма в рублях: {convert_transaction(transaction)}")
```
```
Вывод кода:
    Сумма в рублях: 9150.0  # Пример курса
```

### Processing:
```python
from src.processing import sort_by_date, filter_by_state

dict_list = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 2, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

print(f"Executed: {filter_by_state(dict_list)}")
```
```
Вывод кода:
    Executed: [{'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}]
```

### Decorators:
```python
from src.decorators import log

@log()
def multiply(x, y):
    return x * y

multiply(2, 5)
```
```
Вывод кода:
    Starting function multiply
    Function result: 10
    Finishing...
```
