import pandas as pd


def read_from_file(path_to_file: str, sep: str = ",") -> list:
    """
    Function for reading transactions from CSV or XLSX files.
    Args:
        path_to_file: Path to your file
        sep: Separator for your CSV file
    Returns:
        List of dictionary with operations.
    """
    try:
        if path_to_file.lower().endswith("csv"):
            dataframe = pd.read_csv(path_to_file, sep=sep)
        elif path_to_file.lower().endswith("xlsx"):
            dataframe = pd.read_excel(path_to_file)
        else:
            raise ValueError("This type of file doesn't support")
        dataframe = dataframe.fillna(
            {
                "id": 0,
                "state": "",
                "date": "",
                "amount": 0,
                "currency_name": "",
                "currency_code": "",
                "from": "",
                "to": "",
                "description": "",
            }
        )
        dataframe["id"] = dataframe["id"].astype("Int64")
        return dataframe.to_dict(orient="records")
    except FileNotFoundError:
        return []
