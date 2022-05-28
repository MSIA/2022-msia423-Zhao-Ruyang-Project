import logging

import joblib
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


def df_split(feature_path: str, target_path: str, test_size: float) -> list:
    features = np.load(feature_path, allow_pickle=True)
    target = np.load(target_path, allow_pickle=True)
    if test_size == 0:
        return features, None, target, None
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=test_size)
    return X_train, X_test, y_train, y_test


def split_save(feature_path: str,
               target_path: str,
               test_size: float,
               train_path: str,
               test_path: str) -> None:
    X_train, X_test, y_train, y_test = df_split(feature_path, target_path, test_size)
    X_train_path = train_path + '/X_train.npy'
    y_train_path = train_path + '/y_train.npy'
    X_test_path = test_path + '/X_test.npy'
    y_test_path = test_path + '/y_test.npy'
    np.save(X_train_path, X_train)
    np.save(X_test_path, X_test)
    np.save(y_train_path, y_train)
    np.save(y_test_path, y_test)


def train_and_save(model: sklearn.base.BaseEstimator,
                   X_train_path: str,
                   y_train_path: str,
                   save_path: str) -> None:
    X_train = np.load(X_train_path, allow_pickle=True)
    y_train = np.load(y_train_path, allow_pickle=True)
    model.fit(X_train, y_train)
    joblib.dump(model, save_path)
