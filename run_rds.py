import logging.config

from config.flaskconfig import SQLALCHEMY_DATABASE_URI, LOGGING_CONFIG
from src.sql_util import create_db, UserRecords

logging.config.fileConfig(LOGGING_CONFIG)
logger = logging.getLogger('run_rds.py')

print(SQLALCHEMY_DATABASE_URI)
create_db(SQLALCHEMY_DATABASE_URI)

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()

# our_user = session.query(UserRecords).all()
# print(our_user)