import json


def load_operations(path_to_json: str) -> list:
    """Function for loading operations from json.

    Args:
        path_to_json: Path to operations JSON. If empty, return list.

    Returns:
        Dictionary list."""

    try:
        with open(path_to_json, "r", encoding="utf8") as f:
            operations = json.load(f)
            if not isinstance(operations, list) or not operations:
                operations = list()
    except (ValueError, FileNotFoundError):
        operations = list()
    return operations
