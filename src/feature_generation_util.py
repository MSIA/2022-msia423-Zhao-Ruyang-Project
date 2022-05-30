import logging
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

logger = logging.getLogger(__name__)


def extract_features(read_path: str, save_path: str, target_name: str, feature_names: list = None) -> None:
    """Get the features and target from the dataframe and save them separately

    Args:
        read_path (str): the path to read the dataframe
        save_path (str): the path to save the dataframe
        target_name (str): the name of the target column
        feature_names (:obj: `list` of `str`): a list of feature names to be extracted,
                      if not provided, all columns besides the target will be used
    """
    try:
        df = pd.read_csv(read_path)
    except FileNotFoundError as e:
        logger.error('Path %s does not exist.', read_path)
        raise e
    except pd.errors.ParserError as e:
        logger.error('Wrong file type in %s', read_path)
        raise e
    else:
        logger.info('Successfully read the csv from %s', read_path)
        logger.debug('The shape of the loaded dataframe is: %s', df.shape)

    # Make sure the dataframe contains all the columns in feature_names and target
    target_set = set([target_name])
    if feature_names:
        feature_set = set(feature_names)
    else:
        feature_set = set([])
    column_set = set(df.columns)

    # print(target_set)
    # print(column_set)
    # print(target_set.issubset(column_set))
    # print(feature_set)
    # sys.exit()
    if not (target_set.issubset(column_set) and feature_set.issubset(column_set)):
        logger.error('The columns of the dataframe does not contain all the provided features and targets.')
        raise KeyError('Invalid key for the columns.')
    # Get the target and features respectively
    target = np.array(df[target_name])
    if feature_names:
        features = df[feature_names]
    else:
        features = df.drop(target_name, axis=1)
    # Assemble the full path to save the files
    target_path = save_path + '/target.npy'
    features_path = save_path + '/features.csv'
    # Save the target as npy and features as csv
    try:
        np.save(target_path, target)
        features.to_csv(features_path, index=False)
    except FileNotFoundError as e:
        logger.error('Path does not exist, %s', e)
        raise e
    else:
        logger.info('Successfully saved the features and targets.')


def encode_and_save(read_path: str,
                    encoded_path: str,
                    encoder_path: str,
                    features: list) -> None:
    """Encode the features, save the encoded features and the encoder model

    Args:
        read_path (str): path to read the features file
        encoded_path (str): path to save the encoded features
        encoder_path (str): path to save the encoder model object
        features (:obj:`list` of `str`): feature names that need onehot encoding
    """
    try:
        data = pd.read_csv(read_path)
    except FileNotFoundError as e:
        logger.error('Path %s does not exist.', read_path)
        raise e
    except pd.errors.ParserError as e:
        logger.error('Wrong file type in %s', read_path)
        raise e
    else:
        logger.info('Successfully read the csv from %s', read_path)
        logger.debug('The shape of the loaded dataframe is: %s', data.shape)

    column_names = np.array(data.columns)
    feature_set = set(features)
    column_set = set(column_names)
    if not feature_set.issubset(column_set):
        logger.error('The columns of the dataframe does not contain all the provided features')
        raise KeyError('Invalid feature names.')

    # Get the column index of the features to be encoded
    feature_indices = np.where(np.isin(column_names, features))[0]
    # Initialize the ColumnTransformer
    transformer = ColumnTransformer([('encoder', OneHotEncoder(sparse=False), feature_indices)],
                                    remainder='passthrough')

    data = transformer.fit_transform(data)
    logger.info('Fit and transformed the data successfully.')
    logger.debug('The shape of the transformed data is %s', data.shape)
    try:
        np.save(encoded_path, data)
        joblib.dump(transformer, encoder_path)
    except FileNotFoundError as e:
        logger.error('Path does not exist, %s', e)
        raise e
    else:
        logger.info('Successfully saved the encoded features and encoder.')
