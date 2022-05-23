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
if SQLALCHEMY_DATABASE_URI is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'

# Data path
LOCAL_DATA_PATH = "data/raw/flights_fares_data.csv"
S3_DATA_PATH = "s3://2022-msia423-zhao-ruyang/raw/flights_fares_data.csv"
