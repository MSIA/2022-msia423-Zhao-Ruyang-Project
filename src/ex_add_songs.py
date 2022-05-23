"""Creates, ingests data into, and enables querying of a table of
 songs for the PennyLane app to query from and display results to the user."""
# mypy: plugins = sqlmypy, plugins = flasksqlamypy
import argparse
import logging.config
import sqlite3
import typing

import flask
import sqlalchemy
import sqlalchemy.orm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)

Base: typing.Any = declarative_base()


class Tracks(Base):
    """Creates a data model for the database to be set up for capturing songs.
    """

    __tablename__ = 'tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                              nullable=False)
    artist = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                               nullable=False)
    album = sqlalchemy.Column(sqlalchemy.String(100), unique=False,
                              nullable=True)

    def __repr__(self):
        return f'<Track {self.title}>'


class TrackManager:
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

    def close(self) -> None:
        """Closes SQLAlchemy session

        Returns: None

        """
        self.session.close()

    def add_track(self, title: str, artist: str, album: str) -> None:
        """Seeds an existing database with additional songs.

        Args:
            title (str): Title of song to add to database
            artist (str): Artist of song to add to database
            album (str): Album of song to add to database

        Returns:
            None
        """

        session = self.session
        track = Tracks(artist=artist, album=album, title=title)
        session.add(track)
        session.commit()
        logger.info("%s by %s from album, %s, added to database", title,
                    artist, album)


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


def add_song(args: argparse.Namespace) -> None:
    """Parse command line arguments and add song to database.

    Args:
        args (:obj:`argparse.Namespace`): object containing the following
            fields:

            - args.title (str): Title of song to add to database
            - args.artist (str): Artist of song to add to database
            - args.album (str): Album of song to add to database
            - args.engine_string (str): SQLAlchemy engine string specifying
              which database to write to

    Returns:
        None
    """
    track_manager = TrackManager(engine_string=args.engine_string)
    try:
        track_manager.add_track(args.title, args.artist, args.album)
    except sqlite3.OperationalError as e:
        logger.error(
            "Error page returned. Not able to add song to local sqlite "
            "database: %s. Is it the right path? Error: %s ",
            args.engine_string, e)
    except sqlalchemy.exc.OperationalError as e:
        logger.error(
            "Error page returned. Not able to add song to MySQL database.  "
            "Please check engine string and VPN. Error: %s ", e)
    track_manager.close()
