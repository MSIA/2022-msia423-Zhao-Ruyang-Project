import logging

import joblib
import numpy as np

logger = logging.getLogger(__name__)


def predict_and_save(model_path: str,
                     X_test_path: str,
                     save_path: str,
                     features: list = None) -> None:
    X_test = np.load(X_test_path, allow_pickle=True)
    if features:
        X_test = X_test[features]
    model = joblib.load(model_path)
    y_pred = model.predict(X_test)
    np.save(save_path, y_pred)
