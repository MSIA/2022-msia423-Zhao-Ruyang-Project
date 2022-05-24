import logging.config

import pandas as pd

from config.model_config import LOCAL_DATA_PATH, CLEANED_DATA_PATH
from src.preprocess_util import save_data, convert_column

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('preprocess')

# Preprocess the data
# Read in the data frame
try:
    df = pd.read_csv(LOCAL_DATA_PATH, index_col=0)
except FileNotFoundError as e:
    logger.error('Could not find data in %s', LOCAL_DATA_PATH)
    raise e
except Exception as e:
    logger.error('Failed to load data.')
    logger.error(e)
    raise e

# Define the lookup_map to process the 'stops' column
stop_map = {
    'zero': 0,
    'one': 1,
    'two_or_more': 2
}
processed_df = convert_column(df, 'stops', stop_map)

try:
    save_data(processed_df, CLEANED_DATA_PATH)
except OSError as e:
    logger.error('Path `%s` does not exist.', CLEANED_DATA_PATH)
else:
    logger.info('Cleaned dataframe saved to %s', CLEANED_DATA_PATH)
