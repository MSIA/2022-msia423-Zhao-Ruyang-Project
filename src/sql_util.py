"""Creates, ingests data into, and enables querying of a table of
 songs for the PennyLane app to query from and display results to the user."""
# mypy: plugins = sqlmypy, plugins = flasksqlamypy
import logging.config
import typing
from random import randint
import flask
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select


logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class UserRecords(Base):
    """Creates a data model for the database to be set up for capturing user inputs.
    """

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
        result = session.execute(select(UserRecords.id)).fetchall()
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
                 id: int,
                 airline: str,
                 depart_time: str,
                 source: str,
                 destination:str,
                 stops: int,
                 flight_class: str,
                 duration: int,
                 days_left: int,
                 cur_price: int
                 ) -> None:
        """Adds user record to the user_record table.

        Args:
            id (int): primary key in the table
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
        user_record = UserRecords(id=id,
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
        session.commit()
        logger.info(f'One user record with price {cur_price} added to database.')
        out = session.query(UserRecords).all()
        logger.info(out)

    def add_output(self,
                   id: int,
                   record_id: int,
                   days_left: int,
                   price: int):

        session = self.session
        model_output = ModelOutputs(record_id=record_id,
                                    days_left=days_left,
                                    price=price)
        session.add(model_output)
        session.commit()
        logger.info('Model output added to database.')

    def add_all_output(self,
                       record_id: int,
                       days_left: int,
                       price_list: list):
        session = self.session
        for day in range(days_left):
            model_output = ModelOutputs(record_id=record_id,
                                        days_left=day,
                                        price=price_list[day])
            session.add(model_output)
        session.commit()
        logger.info('All model outputs added to database.')

def create_db(engine_string: str) -> None:
    """Create database with Tracks() data model from provided engine string.

    Args:
        engine_string (str): SQLAlchemy engine string specifying which database
            to write to

    Returns: None

    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Tables successfully created in the database.")

if __name__ == '__main__':
    # pass
    engine_string = 'mysql+pymysql://rzx9163:AWS1998!@nw-msia423-rzx9163.ctarvegaqgdp.us-east-1.rds.amazonaws.com:3306/flight_db'
    engine = sqlalchemy.create_engine(engine_string)
    session_maker = sqlalchemy.orm.sessionmaker(bind=engine)
    session = session_maker()
    result = session.query(ModelOutputs).all()
    for i in result:
        print(i.record_id)