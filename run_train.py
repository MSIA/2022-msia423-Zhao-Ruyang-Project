import pandas as pd
import logging.config
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
# Regression
from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

import yaml


from config.model_config import CLEANED_DATA_PATH, MODEL_PATH

from src.model_util import split_save, train_and_save

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('train_model')

# Preprocess the data
with open('config/model_config.yaml', "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

split_config = config['split_data']
train_config = config['train']

split_save(**split_config)

rm = RandomForestRegressor(n_estimators=30, random_state=123, n_jobs=-1)
train_and_save(rm, **train_config)

# # Output the evaluation metrics of the predictions on the validation set
# logger.info('MSE: %s', mean_squared_error(y_test, rm.predict(X_test)))
# logger.info('MAE: %s', mean_absolute_error(y_test, rm.predict(X_test)))
# logger.info('MAPE: %s', mean_absolute_percentage_error(y_test, rm.predict(X_test)))

