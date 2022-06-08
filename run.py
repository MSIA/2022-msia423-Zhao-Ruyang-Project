import argparse
import logging.config

import pandas as pd
import yaml

from src.evaluation_util import evaluate_model
from src.feature_generation_util import generate_feature
from src.model_util import train_model
from src.prediction_util import score_model
from src.preprocess_util import preprocess_data

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('model-pipeline')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='pipeline for running cloud classification model')

    parser.add_argument('step',
                        default='acquire_data',
                        help='Choose which step to run',
                        choices=['acquire_data', 'preprocess', 'generate_feature',
                                 'train', 'score', 'evaluate'])

    parser.add_argument('--config',
                        default='config/model_config.yaml',
                        help='Path to configuration file')

    args = parser.parse_args()

    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        logger.error('Path %s does not exist.', args.config)
    else:
        logger.info('Successfully loaded configuration file from %s', args.config)

    if args.step == 'preprocess':
        try:
            read_path = config['preprocess']['read_path']
        except KeyError as e:
            logger.error('Key not found.')
            raise e

        try:
            df = pd.read_csv(read_path, index_col=0)
        except FileNotFoundError as e:
            logger.error('Could not find data in %s', read_path)
            raise e
        except Exception as e:
            logger.error('Failed to load data.')
            logger.error(e)
            raise e
        else:
            logger.info('Successfully read the data from %s', read_path)

        preprocess_data(df, config)

    if args.step == 'generate_feature':
        generate_feature(config)

    if args.step == 'train':
        train_model(config)

    if args.step == 'score':
        score_model(config)

    if args.step == 'evaluate':
        evaluate_model(config)
