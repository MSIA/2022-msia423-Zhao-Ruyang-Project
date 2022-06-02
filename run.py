import argparse
import logging.config

import pandas as pd
import yaml
from sklearn.ensemble import RandomForestRegressor

from src.evaluation_util import evaluate_and_save
from src.feature_generation_util import encode_and_save, extract_features
from src.model_util import split_save, train_and_save
from src.prediction_util import predict_and_save
from src.preprocess_util import process_and_save

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('model-pipeline')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="pipeline for running cloud classification model")

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
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        logger.error('Path %s does not exist.', args.config)
    else:
        logger.info("Successfully loaded configuration file from %s", args.config)

    if args.step == 'preprocess':
        try:
            preprocess_config = config['preprocess']
            read_path = preprocess_config['read_path']
            process_param = preprocess_config['process_param']
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

        try:
            process_and_save(df, **process_param)
        except TypeError as e:
            logger.error('Unexpected keyword argument.')
            raise e
        except Exception as e:
            raise e
        else:
            logger.info('Successfully saved the cleaned data.')

    if args.step == 'generate_feature':
        try:
            extract_config = config['generate_feature']['extract_features']
            encode_config = config['generate_feature']['encode']
        except KeyError as e:
            logger.error('Key not found.')
            raise e

        try:
            extract_features(**extract_config)
        except TypeError as e:
            logger.error('Unexpected keyword argument.')
            raise e
        except Exception as e:
            raise e
        else:
            logger.info('Successfully saved the features and targets.')

        try:
            encode_and_save(**encode_config)
        except TypeError as e:
            logger.error('Unexpected keyword argument.')
            raise e
        except Exception as e:
            raise e
        else:
            logger.info('Successfully saved the encoded data and the encoder.')

    if args.step == 'train':
        try:
            split_config = config['split_data']
            train_config = config['train']
            model_param = config['model']
        except KeyError as e:
            logger.error('Key not found.')
            raise e

        try:
            split_save(**split_config)
        except TypeError as e:
            logger.error('Unexpected keyword argument.')
            raise e
        except Exception as e:
            raise e
        else:
            logger.info('Successfully split the data into train and test.')

        rm = RandomForestRegressor(**model_param)
        try:
            train_and_save(rm, **train_config)
        except FileNotFoundError as e:
            logger.error('Invalid path provided in config.')
            raise e
        except TypeError as e:
            logger.error('Unexpected keyword argument.')
            raise e
        except ValueError as e:
            logger.error('Check dimensions of X_train, y_train.')
            raise e
        else:
            logger.info('Successfully trained and saved the RandomForest model.')

    if args.step == 'score':
        try:
            score_config = config['score']
        except KeyError as e:
            logger.error('Key not found.')
            raise e

        try:
            predict_and_save(**score_config)
        except TypeError as e:
            logger.error('Unexpected keyword argument.')
            raise e
        except FileNotFoundError as e:
            logger.error('Invalid path provided in config.')
            raise e
        else:
            logger.info('Successfully saved the price predictions.')

    if args.step == 'evaluate':
        try:
            evaluate_config = config['evaluate']
        except KeyError as e:
            logger.error('Key not found.')
            raise e

        try:
            evaluate_and_save(**evaluate_config)
        except TypeError as e:
            logger.error('Unexpected keyword argument.')
            raise e
        except FileNotFoundError as e:
            logger.error('Invalid path provided in config.')
            raise e
        except ValueError as e:
            logger.error('Check dimensions of labels and predictions.')
            raise e
        else:
            logger.info('Successfully saved the price prediction evaluations')
