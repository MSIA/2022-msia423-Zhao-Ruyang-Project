import logging.config

import pandas as pd
import yaml

from src.preprocess_util import process_and_save

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('preprocess')

# Preprocess the data
with open('config/model_config.yaml', "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
# Read in the data frame
preprocess_config = config['preprocess']
read_path = preprocess_config['read_path']
process_param = preprocess_config['process_param']
try:
    df = pd.read_csv(read_path, index_col=0)
except FileNotFoundError as e:
    logger.error('Could not find data in %s', read_path)
    raise e
except Exception as e:
    logger.error('Failed to load data.')
    logger.error(e)
    raise e

process_and_save(df, **process_param)
