"""Creates, ingests data into, and enables querying of a table of
 songs for the PennyLane app to query from and display results to the user."""
# mypy: plugins = sqlmypy, plugins = flasksqlamypy
import logging.config
import typing

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class FlightRecords(Base):
    """Creates a data model for the database to be set up for capturing songs.
    """

    __tablename__ = 'FlightRecords'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    flight_number = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
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

    def __repr__(self):
        return f'<Flight {self.flight_number} {self.days_left}>'


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
