import sklearn
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)


def df_split(read_path: str, target_name: str, test_size: float) -> list:
    df = pd.read_csv(read_path)
    features = df.drop(target_name, axis=1)
    target = df[target_name]
    if test_size == 0:
        return features, None, target, None
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=test_size)
    return X_train, X_test, y_train, y_test


def split_save(read_path: str,
               target_name: str,
               test_size: float,
               train_path: str,
               test_path: str) -> None:
    X_train, X_test, y_train, y_test = df_split(read_path, target_name, test_size)
    X_train_path = train_path + '/X_train.csv'
    y_train_path = train_path + '/y_train.csv'
    X_test_path = test_path + '/X_test.csv'
    y_test_path = test_path + '/y_test.csv'
    X_train.to_csv(X_train_path, index=False)
    X_test.to_csv(X_test_path, index=False)
    y_train.to_csv(y_train_path, index=False)
    y_test.to_csv(y_test_path, index=False)


def train_and_save(model: sklearn.base.BaseEstimator,
                   X_train_path: str,
                   y_train_path: str,
                   save_path: str,
                   features: list = None) -> None:
    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path).iloc[:, 0]
    if features:
        X_train = X_train[features]
    model.fit(X_train, y_train)
    joblib.dump(model, save_path)


# import logging
# import joblib
# from sklearn.base import BaseEstimator
#
# logger = logging.getLogger(__name__)
#
#
# def save_model(model: BaseEstimator, path: str) -> None:
#     """Save the provided sklearn model to a specified path"""
#     try:
#         joblib.dump(model, path)
#     except FileNotFoundError as e:
#         logger.error('Path `%s` does not exist.', path)
#         raise e
#     except Exception as e:
#         logger.error('Could not save the model.')
#         logger.error(e)
#         raise e
#     else:
#         logger.info('Successfully saved the model to %s', path)
#
#
# def load_model(path: str) -> None:
#     """Load the model from the provided path"""
#     try:
#         model = joblib.load(path)
#     except FileNotFoundError as e:
#         logger.error('Path `%s` does not exist.', path)
#         raise e
#     except Exception as e:
#         logger.error('Could not load the model.')
#         logger.error(e)
#         raise e
#     else:
#         logger.info('Successfully loaded the model.')
#     return model
