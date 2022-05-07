import logging.config

from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.sql_util import create_db

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('run_rds.py')

create_db(SQLALCHEMY_DATABASE_URI)
