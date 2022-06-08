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
    # Check whether column to be converted exist in the dataframe
    if col_name not in df.columns:
        logger.error('The provided dataframe does not have column `%s`.', col_name)
        raise KeyError('Invalid column name.')
    # Create a copy of the provided dataframe
    data = df.copy()
    # Get all unique values in that value
    col_set = set(data[col_name])
    # Get all keys in the provided map
    dict_set = set(lookup_map)
    # Check whether there is unmapped values
    if not col_set.issubset(dict_set):
        logger.warning('The values in %s column is not a subset of the keys in the lookup_map.', col_name)
    # Convert the column
    data[col_name] = data[col_name].map(lookup_map)
    return data


def process_and_save(df: pd.DataFrame,
                     column_to_modify: str,
                     column_to_drop: list ,
                     lookup_map: dict,
                     save_path: str) -> None:
    """Processed the dataframe by modifying and dropping some columns

    Args:
        df (:obj: `pandas.DataFrame`): a provided dataframe to be modified
        column_to_modify (`str`): name of the column to be modified
        column_to_drop (`str`): name of the column to be dropped
        lookup_map (`dict`): dictionary mapping the original value to the modified value
        save_path (`str`): path to save the processed dataframe
    """
    # Modify columns
    try:
        processed_df = convert_column(df, column_to_modify, lookup_map)
    except KeyError as e:
        logger.error('Key error during converting the columns, check column names.')
        raise e
    else:
        logger.debug('Successfully modified the columns: %s', column_to_modify)
    # Drop unused columns
    try:
        processed_df = processed_df.drop(column_to_drop, axis=1)
    except KeyError as e:
        logger.error('Dataframe does not contain a provided column, `%s`.', e)
        raise e
    else:
        logger.debug('Successfully dropped the columns: %s', column_to_drop)
    # Save the processed data
    try:
        processed_df.to_csv(save_path, index=False)
    except FileNotFoundError as e:
        logger.error('Path %s does not exist.', save_path)
        raise e
    else:
        logger.info('Successfully saved the processed data to %s', save_path)


def preprocess_data(df: pd.DataFrame, config: dict) -> None:
    try:
        process_param = config['preprocess']['process_param']
    except KeyError as e:
        logger.error('Key not found.')
        raise e
    try:
        process_and_save(df, **process_param)
    except TypeError as e:
        logger.error('Unexpected keyword argument.')
        raise e
    except Exception as e:
        raise e
    else:
        logger.info('Successfully saved the cleaned data.')