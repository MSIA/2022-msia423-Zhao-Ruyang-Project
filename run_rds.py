import logging.config

from config.flaskconfig import SQLALCHEMY_DATABASE_URI, LOGGING_CONFIG
from src.sql_util import create_db

logging.config.fileConfig(LOGGING_CONFIG)
logger = logging.getLogger('run_rds.py')

create_db(SQLALCHEMY_DATABASE_URI)
