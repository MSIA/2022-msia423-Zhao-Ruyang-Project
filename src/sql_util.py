"""Creates, ingests data into, and enables querying of a table of
 songs for the PennyLane app to query from and display results to the user."""
# mypy: plugins = sqlmypy, plugins = flasksqlamypy
import logging.config
import typing

import flask
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base


logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class UserRecords(Base):
    """Creates a data model for the database to be set up for capturing songs.
    """

    __tablename__ = 'user_records'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    flight_operator = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                      nullable=True)
    departure_date = sqlalchemy.Column(sqlalchemy.Date, unique=False,
                                       nullable=False)
    departure_time = sqlalchemy.Column(sqlalchemy.Time, unique=False,
                                       nullable=False)
    source_city = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                    nullable=True)
    destination = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                    nullable=True)
    stops = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                              nullable=True)
    total_time = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                   nullable=True)
    days_left = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                  nullable=True)
    cur_price = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                  nullable=True)

    def __repr__(self):
        return f'<Flight {self.flight_number} {self.days_left}>'

class ModelOutputs(Base):
    """Creates a data model for the database to be set up for capturing songs.
    """

    __tablename__ = 'model_outputs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    flight_operator = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                      nullable=True)
    departure_date = sqlalchemy.Column(sqlalchemy.Date, unique=False,
                                       nullable=False)
    departure_time = sqlalchemy.Column(sqlalchemy.Time, unique=False,
                                       nullable=False)
    source_city = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                    nullable=True)
    destination = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                    nullable=True)
    stops = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                              nullable=True)
    total_time = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                   nullable=True)
    days_left = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                  nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)

    def __repr__(self):
        return f'<Flight {self.flight_number} {self.days_left}>'


class RecordManager:
    """Creates a SQLAlchemy connection to the tracks table.

    Args:
        app (:obj:`flask.app.Flask`): Flask app object for when connecting from
            within a Flask app. Optional.
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to. Follows the format
    """
    def __init__(self, app: typing.Optional[flask.app.Flask] = None,
                 engine_string: typing.Optional[str] = None):
        if app:
            self.database = SQLAlchemy(app)
            self.session = self.database.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            session_maker = sqlalchemy.orm.sessionmaker(bind=engine)
            self.session = session_maker()
        else:
            raise ValueError(
                "Need either an engine string or a Flask app to initialize")


def create_db(engine_string: str) -> None:
    """Create database with Tracks() data model from provided engine string.

    Args:
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to

    Returns: None

    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")



