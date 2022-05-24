import pandas as pd
import logging.config
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
# Regression
from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import joblib

from src.model_util import save_model
from config.model_config import CLEANED_DATA_PATH, MODEL_PATH

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('train_model')

df = pd.read_csv(CLEANED_DATA_PATH)
data = pd.get_dummies(df)


X = data.drop('price', axis=1)
y = data['price']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=123)
rm = RandomForestRegressor(n_estimators=300, random_state=123, n_jobs=-1, oob_score=True)
rm.fit(X_train, y_train)

# Output the evaluation metrics of the predictions on the validation set
logger.info('MSE: %s', mean_squared_error(y_test, rm.predict(X_test)))
logger.info('MAE: %s', mean_absolute_error(y_test, rm.predict(X_test)))
logger.info('MAPE: %s', mean_absolute_percentage_error(y_test, rm.predict(X_test)))

#Save the model
save_model(rm, MODEL_PATH)