import logging

import joblib
import numpy as np

logger = logging.getLogger(__name__)


def predict_and_save(model_path: str,
                     x_test_path: str,
                     save_path: str) -> None:
    """Make predictions on a given test set with a given model, and save the predictions to specified path

    Args:
        model_path (str): path to load the model
        x_test_path (str): path to load the test set
        save_path (str): path to save the predictions
    """
    try:
        x_test = np.load(x_test_path, allow_pickle=True)
    except FileNotFoundError as e:
        logger.error('Path %s does not exist. Failed to load the test data.', x_test_path)
        raise e
    else:
        logger.info('Successfully loaded the test data from %s', x_test_path)
    try:
        model = joblib.load(model_path)
    except FileNotFoundError as e:
        logger.error('Path %s does not exist. Failed to load the model.', model_path)
        raise e
    else:
        logger.info('Successfully loaded the model from %s', model_path)

    try:
        y_pred = model.predict(x_test)
    except ValueError as e:
        logger.error('x_test does not have correct number of dimensions.')
        raise e
    else:
        logger.info('Successfully made the prediction.')
        logger.debug('There are %s predictions made.', len(y_pred))

    try:
        np.save(save_path, y_pred)
    except FileNotFoundError as e:
        logger.error('Path %s does not exist. Failed to save the predictions.', save_path)
        raise e
    else:
        logger.info('Successfully saved the predictions to %s.', save_path)
