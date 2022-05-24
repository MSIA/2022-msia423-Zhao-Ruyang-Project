import logging
import joblib
from sklearn.base import BaseEstimator

logger = logging.getLogger(__name__)


def save_model(model: BaseEstimator, path: str) -> None:
    """Save the provided sklearn model to a specified path"""
    try:
        joblib.dump(model, path)
    except FileNotFoundError as e:
        logger.error('Path `%s` does not exist.', path)
        raise e
    except Exception as e:
        logger.error('Could not save the model.')
        logger.error(e)
        raise e
    else:
        logger.info('Successfully saved the model to %s', path)


def load_model(path: str) -> None:
    """Load the model from the provided path"""
    try:
        model = joblib.load(path)
    except FileNotFoundError as e:
        logger.error('Path `%s` does not exist.', path)
        raise e
    except Exception as e:
        logger.error('Could not load the model.')
        logger.error(e)
        raise e
    else:
        logger.info('Successfully loaded the model.')
    return model
