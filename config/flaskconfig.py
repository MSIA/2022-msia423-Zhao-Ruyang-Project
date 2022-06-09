import os
DEBUG = True
LOGGING_CONFIG = 'config/logging/local.conf'
HOST = '0.0.0.0'
PORT = 5001
APP_NAME = 'flight-price-prediction'
SQLALCHEMY_TRACK_MODIFICATIONS = True #If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals.
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/flight.db'
