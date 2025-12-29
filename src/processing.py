def filter_by_state(dict_list: list, state: str = "EXECUTED") -> list:
    """Getting dictionary list and state, returning dictionary list with this state"""
    filtered_list = []
    for dictionary in dict_list:
        if dictionary["state"] != state:
            continue
        filtered_list.append(dictionary)
    return filtered_list


def sort_by_date(dict_list: list, sort_by_decreasing: bool = True) -> list:
    """Getting dictionary list and boolean variable for sort by decreasing, returning sorted list"""
    return sorted(dict_list, key=lambda x: x["date"], reverse=sort_by_decreasing)
