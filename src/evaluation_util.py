import logging

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

logger = logging.getLogger(__name__)


def evaluate_and_save(prediction_path: str,
                      ytrue_path: str,
                      save_path: str) -> None:
    """Evaluate the given predictions based on true labels, save the evaluations to specified path

    Args:
        prediction_path (str): path to load the predictions
        ytrue_path (str): path to load the true labels
        save_path (str): path to save the evaluation metrics
    """
    try:
        y_true = np.load(ytrue_path, allow_pickle=True)
        y_pred = np.load(prediction_path, allow_pickle=True)
    except FileNotFoundError as e:
        logger.error('Invalid path provided for np.load(). Failed to load prediction and true label.')
        raise e
    else:
        logger.info('Successfully loaded predictions and true labels.')
    try:
        mse = mean_squared_error(y_pred, y_true)
        mae = mean_absolute_error(y_pred, y_true)
        mape = mean_absolute_percentage_error(y_pred, y_true)
    except ValueError as e:
        logger.error('The y_pred(%s) and y_true(%s) do not have same length.', len(y_pred), len(y_true))
        raise e
    else:
        logger.info('Successfully calculated evaluation metrics.')
    # Assemble the report statement
    mse_str = 'MSE of price predictions: %s' % mse
    mae_str = 'MAE of price predictions: %s' % mae
    mape_str = 'MAPE of price predictions: %s' % mape
    logger.info(mse_str)
    logger.info(mae_str)
    logger.info(mape_str)
    # Write the report to a txt file
    try:
        with open(save_path, 'w') as f:
            f.write(mse_str + '\n')
            f.write(mae_str + '\n')
            f.write(mape_str + '\n')
    except FileNotFoundError as e:
        logger.error('Path %s does not exist. Failed to save the report.', save_path)
        raise e
    else:
        logger.info('Successfully saved the evaluation metrics to %s', save_path)
