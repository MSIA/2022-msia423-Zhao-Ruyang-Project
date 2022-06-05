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
        logger.error('Invalid path provided for np.load(). '
                     'Failed to load prediction and true label.')
        raise e
    else:
        logger.info('Successfully loaded predictions and true labels.')
    try:
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred)
    except ValueError as e:
        logger.error('The y_pred(%s) and y_true(%s) do not have same length.',
                     len(y_pred), len(y_true))
        raise e
    else:
        logger.info('Successfully calculated evaluation metrics.')
    # Assemble the report statement
    mse_str = f'MSE of price predictions: {mse}'
    mae_str = f'MAE of price predictions: {mae}'
    mape_str = f'MAPE of price predictions: {mape}'
    logger.info(mse_str)
    logger.info(mae_str)
    logger.info(mape_str)
    # Write the report to a txt file
    try:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(mse_str + '\n')
            file.write(mae_str + '\n')
            file.write(mape_str + '\n')
    except FileNotFoundError as e:
        logger.error('Path %s does not exist. Failed to save the report.', save_path)
        raise e
    else:
        logger.info('Successfully saved the evaluation metrics to %s', save_path)
