from typing import NotRequired, TypedDict

from src.csv_xlsx_reader import read_from_file
from src.generators import filter_by_currency
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import load_operations
from src.widget import get_date, mask_account_card


class UserPreferences(TypedDict):
    status: str
    sort_by_date: bool
    sort_by_increase: bool
    sort_by_currency: bool
    sort_by_keyword: bool
    keyword: NotRequired[str]
    file_type: str


FILE_PATHS = {
    "JSON": "../data/operations.json",
    "CSV": "../data/transactions.csv",
    "XLSX": "../data/transactions_excel.xlsx",
}


def ask(prompt: str) -> str:
    print(f"Программа:\n{prompt}")
    return input("Пользователь: ").strip()


def ask_choice(
    prompt: str, valid_choices: list[str], default: str | None = None, error_message: str | None = None
) -> str:
    while True:
        raw_answer = ask(prompt)
        answer = raw_answer.upper()
        if answer in valid_choices:
            return answer
        if default is not None:
            print(f"Программа:\nВыбрано значение по умолчанию: {default}")
            return default.upper()
        if error_message is not None:
            print(f"Программа:\n{error_message.format(raw_answer)}")
        else:
            print(f"Программа:\nНекорректный ввод, возможные варианты:\n{", ".join(valid_choices)}")


def get_user_preferences() -> UserPreferences:
    prefs: UserPreferences = {
        "status": "",
        "sort_by_date": False,
        "sort_by_increase": False,
        "sort_by_currency": False,
        "sort_by_keyword": False,
        "file_type": "",
    }
    prefs["status"] = ask_choice(
        "Введите статус, по которому необходимо выполнить фильтрацию."
        "\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING",
        ["EXECUTED", "CANCELED", "PENDING"],
        error_message='Статус операции "{}" недоступен.',
    )
    print(f'Программа:\nОперации отфильтрованы по статусу "{prefs["status"]}"')
    prefs["sort_by_date"] = ask_choice("Отсортировать операции по дате?(Да/нет)", ["ДА", "НЕТ"], "да") == "ДА"
    prefs["sort_by_increase"] = (
        ask_choice("Отсортировать по возрастанию или по убыванию?(1/2)", ["1", "2"], "1") == "2"
    )
    prefs["sort_by_currency"] = ask_choice("Выводить только рублевые транзакции?(Да/нет)", ["ДА", "НЕТ"], "да") == "ДА"
    prefs["sort_by_keyword"] = (
        ask_choice("Отфильтровать список транзакций по определенному слову в описании? (Да/Нет)", ["ДА", "НЕТ"])
        == "ДА"
    )
    if prefs["sort_by_keyword"]:
        prefs["keyword"] = ask("Введите ключевое слово")
    return prefs


def format_operation(operation: dict) -> str:
    date_str = get_date(operation["date"])
    description = operation["description"]
    amount = float(operation["operationAmount"]["amount"])
    amount_str = str(int(amount)) if amount == int(amount) else str(amount)
    currency = operation["operationAmount"]["currency"]["name"]

    lines = [f"{date_str} {description}"]
    from_field = operation.get("from", "")
    to_field = operation.get("to", "")
    if from_field:
        lines.append(f"{mask_account_card(from_field)} -> {mask_account_card(to_field)}")
    else:
        lines.append(mask_account_card(to_field))
    lines.append(f"Сумма: {amount_str} {currency}")
    return "\n".join(lines)


def main() -> None:
    file_types = ["JSON", "CSV", "XLSX"]
    print("Программа:\n" "Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    for i, file in enumerate(file_types, start=1):
        print(f"{i}. Получить информацию о транзакциях из {file}-файла")
    file_choice = ask_choice("Выберите необходимый пункт меню", ["1", "2", "3"])
    file_type = file_types[int(file_choice) - 1]
    print(f"Программа:\nДля обработки выбран {file_type}-файл")

    prefs = get_user_preferences()
    prefs["file_type"] = file_type
    if prefs["file_type"] != "JSON":
        operations = read_from_file(FILE_PATHS[prefs["file_type"]], sep=";")
    else:
        operations = load_operations(FILE_PATHS[prefs["file_type"]])
    if operations == [] or operations is None:
        print("Ошибка: Файл не найден!")
        return
    filtered_operations = filter_by_state(operations, state=prefs["status"])
    if prefs["sort_by_date"]:
        filtered_operations = sort_by_date(filtered_operations, prefs["sort_by_increase"])
    if prefs["sort_by_currency"]:
        filtered_operations = list(filter_by_currency(filtered_operations, "rub"))
    if prefs["sort_by_keyword"]:
        filtered_operations = process_bank_search(filtered_operations, prefs["keyword"])
    if not list(filtered_operations):
        print("Программа:\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print("Программа:\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_operations)}")
    for operation in filtered_operations:
        print()
        print(format_operation(operation))


if __name__ == "__main__":
    main()
