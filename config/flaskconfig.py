import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5001
APP_NAME = "flight-price-prediction"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rzx9163:Aws1998!@nw-msia423-rzx9163.ctarvegaqgdp.us-east-1.rds.amazonaws.com:3306/test'
if SQLALCHEMY_DATABASE_URI is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'

# Data path
LOCAL_DATA_PATH = "data/raw/flight_data.csv"
S3_DATA_PATH = "s3://2022-msia423-zhao-ruyang/raw/flight_data.csv"
