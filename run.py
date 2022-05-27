import logging.config
import argparse
import yaml
from src.preprocess_util import process_and_save
import pandas as pd
from src.model_util import split_save, train_and_save
from sklearn.ensemble import RandomForestRegressor

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('model-pipeline')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="pipeline for running cloud classification model")

    parser.add_argument('step',
                        default='acquire_data',
                        help='Which step to run',
                        choices=['acquire_data', 'preprocess', 'generate_feature',
                                 'train', 'score', 'evaluate'])

    parser.add_argument('--config',
                        default='config/model_config.yaml',
                        help='Path to configuration file')

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    logger.info("Configuration file loaded from %s" % args.config)

    if args.step == 'preprocess':
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

    if args.step == 'train':
        split_config = config['split_data']
        train_config = config['train']

        split_save(**split_config)

        rm = RandomForestRegressor(n_estimators=30, random_state=123, n_jobs=-1)
        train_and_save(rm, **train_config)