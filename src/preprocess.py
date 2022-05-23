import pandas as pd


def convert_column(df: pd.DataFrame, col_name: str, map: dict) -> pd.DataFrame:
    """Return a dataframe with a certain column modified according to the provided dictionary

    Args:
        df (:obj: `pandas.DataFrame`): a provided dataframe to be modified
        col_name (`str`): name of the column to be modified
        map (`dict`): dictionary mapping the original value to the modified value

    Returns:
        data (:obj: `pandas.DataFrame`): a modified dataframe
    """
    # Create a copy of the provided dataframe
    data = df.copy()
    # Convert the column
    data[col_name] = data[col_name].map(map)
    return data


def save_data(df: pd.DataFrame, path: str) -> None:
    """Save the data into a specified path

    Args:
        df (:obj: `pandas.DataFrame`): a provided dataframe to be saved
        path (`str`): path to save data
    """
    df.to_csv(path)