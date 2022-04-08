"""Configures the subparsers for receiving command line arguments for each
 stage in the model pipeline and orchestrates their execution."""
import argparse
import logging.config

from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.add_songs import create_db, add_song

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('penny-lane-pipeline')

if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(
        description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for creating a database
    sp_create = subparsers.add_parser("create_db",
                                      description="Create database")
    sp_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data
    sp_ingest = subparsers.add_parser("ingest",
                                      description="Add data to database")
    sp_ingest.add_argument("--artist", default="Emancipator",
                           help="Artist of song to be added")
    sp_ingest.add_argument("--title", default="Minor Cause",
                           help="Title of song to be added")
    sp_ingest.add_argument("--album", default="Dusk to Dawn",
                           help="Album of song being added")
    sp_ingest.add_argument("--engine_string",
                           default='sqlite:///data/tracks.db',
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        add_song(args)
    else:
        parser.print_help()
