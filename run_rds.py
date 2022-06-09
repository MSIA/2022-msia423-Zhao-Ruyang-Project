import logging.config

import sqlalchemy

from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.sql_util import create_db

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('create_sql_database')

if __name__ == '__main__':
    try:
        create_db(SQLALCHEMY_DATABASE_URI)
    except sqlalchemy.exc.ArgumentError as e:
        logger.error('Could not parse URL from the engine string. %s', e)
        raise e
    except sqlalchemy.exc.OperationalError as e:
        logger.error('Could not establish connection. Check engine string. %s', e)
        raise e
    else:
        logger.info('Successfully created the tables')
