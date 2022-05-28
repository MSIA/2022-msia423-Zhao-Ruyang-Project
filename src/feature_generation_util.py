from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
import joblib


def extract_features(read_path: str, save_path: str, target_name: str, feature_names: list = None) -> None:
    df = pd.read_csv(read_path)
    target = np.array(df[target_name])
    if feature_names:
        features = df[feature_names]
    else:
        features = df.drop(target_name, axis=1)
    target_path = save_path + '/target.npy'
    features_path = save_path + '/features.csv'
    np.save(target_path, target)
    features.to_csv(features_path, index=False)


def encode_and_save(read_path: str,
                    encoded_path: str,
                    encoder_path: str,
                    features: list) -> None:

    data = pd.read_csv(read_path)
    column_names = np.array(data.columns)
    feature_indices = np.where(np.isin(column_names, features))[0]

    transformer = ColumnTransformer([('encoder', OneHotEncoder(sparse=False), feature_indices)],
                                    remainder='passthrough')

    data = transformer.fit_transform(data)
    np.save(encoded_path, data)
    joblib.dump(transformer, encoder_path)
