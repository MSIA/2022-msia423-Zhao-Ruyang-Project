import logging
import pandas as pd

logger = logging.getLogger(__name__)


def convert_column(df: pd.DataFrame, col_name: str, lookup_map: dict) -> pd.DataFrame:
    """Return a dataframe with a certain column modified according to the provided dictionary

    Args:
        df (:obj: `pandas.DataFrame`): a provided dataframe to be modified
        col_name (`str`): name of the column to be modified
        lookup_map (`dict`): dictionary mapping the original value to the modified value

    Returns:
        data (:obj: `pandas.DataFrame`): a modified dataframe
    """
    # Create a copy of the provided dataframe
    if col_name not in df.columns:
        logger.error('The provided dataframe does not have column `%s`.', col_name)
        raise KeyError('Invalid column name.')
    data = df.copy()
    col_set = set(data[col_name])
    dict_set = set(lookup_map)
    if not col_set.issubset(dict_set):
        logger.warning('The values in %s column is not a subset of the keys in the lookup_map.', col_name)
    # Convert the column
    data[col_name].unique()
    data[col_name] = data[col_name].map(lookup_map)
    return data


def save_data(df: pd.DataFrame, path: str) -> None:
    """Save the data into a specified path

    Args:
        df (:obj: `pandas.DataFrame`): a provided dataframe to be saved
        path (`str`): path to save data
    """
    try:
        df.to_csv(path, index=False)
    except OSError as e:
        logger.error('Path `%s` does not exist.', path)
        raise e
    else:
        logger.info('Data successfully saved to %s', path)
