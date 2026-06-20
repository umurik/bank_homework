import re
from collections import Counter


def filter_by_state(dict_list: list, state: str = "EXECUTED") -> list:
    """Getting dictionary list and state, returning dictionary list with this state"""
    if state is None:
        raise ValueError("Wrong dictionary list or statement value")
    if not isinstance(dict_list, list):
        raise ValueError("Wrong dictionary list or statement value")
    if state.upper() != "EXECUTED" and state.upper() != "CANCELED" and state.upper() != "PENDING":
        raise ValueError("Wrong dictionary list or statement value")
    state = state.upper()
    filtered_list = []
    for dictionary in dict_list:
        if dictionary.get("state", "") != state:
            continue
        filtered_list.append(dictionary)
    return filtered_list


def sort_by_date(dict_list: list, sort_by_decreasing: bool = True) -> list:
    """Getting dictionary list and boolean variable for sort by decreasing, returning sorted list"""
    if isinstance(dict_list, list) and isinstance(sort_by_decreasing, bool):
        return sorted(dict_list, key=lambda x: x.get("date", ""), reverse=sort_by_decreasing)
    else:
        raise ValueError("Wrong dictionary list or boolean value")


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Function for finding string in list[dict] description.

    Args:
        data: data with bank operations
        search: target string

    Returns:
        Dictionary list of operations with target string.

    """
    if not isinstance(search, str) or not isinstance(data, list) or not data:
        return []
    target_string = re.compile(r"\b" + re.escape(search), flags=re.IGNORECASE)
    result = []
    for operation in data:
        if target_string.search(operation.get("description", "")):
            result.append(operation)
    return result


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Function for counting categories operations in data.

    Args:
        data: data with bank operations
        categories: bank operations categories

    Returns:
        Dictionary with counted categories

    """
    if not isinstance(data, list) or not isinstance(categories, list):
        return {}
    counted_descriptions = Counter(x.get("description", 0) for x in data)
    final_dict = {x: counted_descriptions[x] for x in categories}
    return final_dict
