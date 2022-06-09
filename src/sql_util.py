"""Creates, ingests data into, and enables querying of a table of
 songs for the PennyLane app to query from and display results to the user."""
import logging.config
import typing
from random import randint

import flask
import sqlalchemy
import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class UserRecords(Base):
    """Creates a data model for the database to be set up for capturing user inputs."""
    __tablename__ = 'user_records'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    airline = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                nullable=True)
    departure_time = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                       nullable=False)
    source_city = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                    nullable=True)
    destination = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                    nullable=True)
    stops = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                              nullable=True)
    flight_class = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                                     nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                 nullable=True)
    days_left = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                  nullable=True)
    cur_price = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                  nullable=True)

    def __repr__(self):
        return f'<User_record {self.id}>'


class ModelOutputs(Base):
    """Creates a data model for the database to be set up for capturing model outputs.
    """
    __tablename__ = 'model_outputs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    record_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user_records.id"))

    days_left = sqlalchemy.Column(sqlalchemy.Integer, unique=False,
                                  nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=True)

    def __repr__(self):
        return f'<Model_output {self.id}>'


class RecordManager:
    """Creates a SQLAlchemy connection to the flight_db database.

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

    def close(self) -> None:
        """Closes SQLAlchemy session

        Returns: None
        """
        self.session.close()

    def get_ids(self):
        """Get all primary keys of the user_record table"""
        session = self.session
        try:
            result = session.execute(select(UserRecords.id)).fetchall()
        except sqlalchemy.exc.OperationalError as e:
            logger.error('Unable to get ids from user_records table. Check network.')
            raise e
        except sqlalchemy.exc.SQLAlchemyError as e:
            logger.error('Unable to get ids from user_records table')
            raise e

        ids = [row[0] for row in result]
        return ids

    def unique_id(self):
        """Generate an id that does not exist in the user_record table"""
        existing_ids = self.get_ids()
        record_id = randint(1, 10000)
        while record_id in existing_ids:
            record_id = randint(1, 10000)
        return record_id

    def add_user(self,
                 _id: int,
                 airline: str,
                 depart_time: str,
                 source: str,
                 destination: str,
                 stops: int,
                 flight_class: str,
                 duration: int,
                 days_left: int,
                 cur_price: int
                 ) -> None:
        """Adds user record to the user_record table.

        Args:
            _id (int): primary key in the table
            airline (str): airline name
            depart_time (str): time of departure
            source (str): departure city name
            destination (str): destination city name
            stops (int): number of stops
            flight_class (str): flight class, economy or business
            duration (int): duration of flight in hours
            days_left (int): days before departure
            cur_price (int): price in Indian rupee
        Returns:
            None
        """

        session = self.session
        user_record = UserRecords(id=_id,
                                  airline=airline,
                                  departure_time=depart_time,
                                  source_city=source,
                                  destination=destination,
                                  stops=stops,
                                  flight_class=flight_class,
                                  duration=duration,
                                  days_left=days_left,
                                  cur_price=cur_price)
        session.add(user_record)
        try:
            session.commit()
        except sqlalchemy.exc.OperationalError as e:
            logger.error('Unable to add user record to user_records table. Check network.')
            raise e
        except sqlalchemy.exc.SQLAlchemyError as e:
            logger.error('Unable to add user record to user_records table')
            raise e
        else:
            logger.info(f'One user record with price {cur_price} added to database.')

    def add_output(self,
                   record_id: int,
                   days_left: int,
                   price: int) -> None:
        """Add a model output to the model_outputs table

        Args:
            record_id (int): the record_id of the model output
            days_left (int): days left before departure
            price (int): predicted price of the flight
        """
        session = self.session
        model_output = ModelOutputs(record_id=record_id,
                                    days_left=days_left,
                                    price=price)
        session.add(model_output)
        try:
            session.commit()
        except sqlalchemy.exc.OperationalError as e:
            logger.error('Unable to add model output to model_outputs table. Check network.')
            raise e
        except sqlalchemy.exc.SQLAlchemyError as e:
            logger.error('Unable to add model output to model_outputs table')
            raise e
        else:
            logger.info(f'Added predicted price of {record_id} with {days_left} days left.')

    def add_all_output(self,
                       record_id: int,
                       days_left: int,
                       price_list: list):
        """Add predicted prices of a flight from current day to last day

        Args:
            record_id (int): the record_id associated to the user record
            days_left (int): days left before departure
            price_list (`list` of `int`): list of predicted price for all days up to the departure day
        """
        # Get the db session
        session = self.session
        for day in range(days_left):
            model_output = ModelOutputs(record_id=record_id,
                                        days_left=day,
                                        price=price_list[day])
            session.add(model_output)
        try:
            session.commit()
        except sqlalchemy.exc.OperationalError as e:
            logger.error('Unable to add all model outputs to model_outputs table')
            raise e
        except sqlalchemy.exc.SQLAlchemyError as e:
            logger.error('Unable to add model outputs to model_outputs table')
            raise e
        else:
            logger.info(f'All model outputs of {record_id} added to database.')


def create_db(engine_string: str) -> None:
    """Create database with Tracks() data model from provided engine string.

    Args:
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to

    Returns: None

    """
    engine = sqlalchemy.create_engine(engine_string)
    try:
        Base.metadata.create_all(engine)
    except sqlalchemy.exc.ArgumentError as e:
        logger.error('Could not parse URL from the engine string. %s', e)
        raise e
    except sqlalchemy.exc.OperationalError as e:
        logger.error('Could not establish connection. Check engine string. %s', e)
        raise e
    else:
        logger.info("The tables `user_records` and `model_outputs` are successfully created in the database.")


if __name__ == '__main__':
    create_db('sqlite:///data/flight.dbd')
    # engine = sqlalchemy.create_engine(engine_string)
    # session_maker = sqlalchemy.orm.sessionmaker(bind=engine)
    # session = session_maker()
    # result = session.query(ModelOutputs).all()
    # for i in result:
    #     print(i.record_id)
