import logging

import joblib
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


def df_split(feature_path: str, target_path: str, test_size: float, random_state: int) -> list:
    """Split the features and target into train and test
    Args:
        feature_path (str): path to read the features file
        target_path (str): path to read the target file
        test_size (float): proportion of test set relative to the whole dataset
        random_state (int): seed to reproduce the split
    Returns:
        x_train, x_test, y_train, y_test (:obj:`list`of`pd.DataFrame`/`np.array`):
            the list containing the x_train, x_test, y_train, y_test.
    """
    try:
        features = np.load(feature_path, allow_pickle=True)
        target = np.load(target_path, allow_pickle=True)
    except FileNotFoundError as e:
        logger.error('Invalid path when loading the features and target, %s', e)
        raise e
    else:
        logger.info('Successfully loaded the features and target.')
    # return the full features and target as x_train and y_train if test_size == 0
    if test_size == 0:
        return features, None, target, None
    # Split according to the test size if test_size != 0
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=test_size, random_state=random_state)
    logger.info('Successfully split the data into train and test using train_test_split().')
    return x_train, x_test, y_train, y_test


def split_save(feature_path: str,
               target_path: str,
               test_size: float,
               random_state: int,
               train_path: str,
               test_path: str) -> None:
    """Split the features and target and save them in specified path

    Args:
        feature_path (str): path to read the features file
        target_path (str): path to read the target file
        test_size (float): proportion of test set relative to the whole dataset
        random_state (int): seed to reproduce the split
        train_path (str): path to save the train data
        test_path (str): path to save the test data
    """
    try:
        x_train, x_test, y_train, y_test = df_split(feature_path, target_path, test_size, random_state)
    except FileNotFoundError as e:
        logger.error('Invalid path provided to df_split, %s', e)
        raise e
    else:
        logger.info('Successfully split the data into train and test using df_split().')
    # Assemble the complete path to save all the files
    x_train_path = train_path + '/x_train.npy'
    y_train_path = train_path + '/y_train.npy'
    x_test_path = test_path + '/x_test.npy'
    y_test_path = test_path + '/y_test.npy'
    try:
        np.save(x_train_path, x_train)
        np.save(x_test_path, x_test)
        np.save(y_train_path, y_train)
        np.save(y_test_path, y_test)
    except FileNotFoundError as e:
        logger.error('Invalid paths when saving the data after split, %s', e)
        raise e
    else:
        logger.info('Successfully saved the data after split.')


def train_and_save(model: sklearn.base.BaseEstimator,
                   x_train_path: str,
                   y_train_path: str,
                   save_path: str) -> None:
    """Train the passed in model, and save the model in specified path

    Args:
        model (:obj:`sklearn.base.BaseEstimator`): sklearn model to be trained
        x_train_path (str): path to the features of training data
        y_train_path (str): path to the target of the training data
        save_path (str): path to save the trained model
    """
    # Load the data
    try:
        x_train = np.load(x_train_path, allow_pickle=True)
        y_train = np.load(y_train_path, allow_pickle=True)
    except FileNotFoundError as e:
        logger.error('Invalid path when loading the training data, %s', e)
        raise e
    else:
        logger.info('Successfully loaded the training data.')

    # Fit the model
    try:
        model.fit(x_train, y_train)
    except ValueError as e:
        logger.error('The number of rows of x_train is not equal to the length of y_train')
        logger.error(e)
        raise e

    # Save the model
    try:
        joblib.dump(model, save_path)
    except FileNotFoundError as e:
        logger.error('Path `%s` does not exist. Failed to save the model.', save_path)
        raise e
    else:
        logger.info('Successfully saved the model to %s', save_path)
