import logging

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

logger = logging.getLogger(__name__)


def evaluate_and_save(prediction_path: str,
                      ytrue_path: str,
                      save_path: str) -> None:
    y_true = np.load(ytrue_path, allow_pickle=True)
    y_test = np.load(prediction_path, allow_pickle=True)
    mse = mean_squared_error(y_test, y_true)
    mae = mean_absolute_error(y_test, y_true)
    mape = mean_absolute_percentage_error(y_test, y_true)
    mse_str = 'MSE: %s' % mse
    mae_str = 'MAE: %s' % mae
    mape_str = 'MAPE: %s' % mape
    logger.info(mse_str)
    logger.info(mae_str)
    logger.info(mape_str)
    with open(save_path, 'w') as f:
        f.write(mse_str + '\n')
        f.write(mae_str + '\n')
        f.write(mape_str + '\n')
