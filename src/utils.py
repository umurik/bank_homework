import json
import logging
import os

logger = logging.getLogger(__name__)
if not os.path.exists(os.path.join("..", "logs")):
    os.makedirs(os.path.join("..", "logs"))
file_handler = logging.FileHandler(os.path.join("..", "logs", "utils.log"))
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_operations(path_to_json: str) -> list[dict]:
    """Function for loading operations from JSON.

    Args:
        path_to_json: Path to operations JSON. If empty, return list.

    Returns:
        Dictionary list."""

    if path_to_json in ("", None):
        logger.debug("Path is empty, returning empty list")
        return []
    try:
        logger.debug(f"Trying to open file: {path_to_json}")
        with open(path_to_json, "r", encoding="utf8") as f:
            operations = json.load(f)
            logger.debug("Validating JSON")
            if not isinstance(operations, list):
                raise ValueError("JSON data is not a list")
        logger.debug("Operation completed successfully")
    except Exception:
        logger.exception("Error while validating JSON or opening file")
        raise
    return operations
