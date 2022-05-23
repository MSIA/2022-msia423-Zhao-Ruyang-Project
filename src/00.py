import logging

import sqlalchemy
from sqlalchemy import create_engine

# Create a logger
logger = logging.getLogger(__name__)


class RdsUtil:
    def __init__(self, engine_string: str):
        if not engine_string:
            logger.error('ENGINE_STRING is None')
            raise ValueError('None type encountered for ENGINE_STRING.')
        if not isinstance(engine_string, str):
            logger.error('ENGINE_STRING is not a string')
            raise ValueError('Non-string type encountered for ENGINE_STRING.')

        try:
            self.engine = create_engine(engine_string)
        except sqlalchemy.exc.NoSuchModuleError as e:
            logger.error(e)
            logger.error('Unable to connect to the sql engine.')
            raise e
        except Exception as e:
            logger.error(e)
            logger.error('Unable to connect to the sql engine.')
            raise e

    def exec_sql(self, statement: str):
        try:
            with self.engine.connect() as con:
                try:
                    con.execute(statement)
                except sqlalchemy.exc.ProgrammingError as e:
                    logger.error(e)
                    logger.error('Unable to execute the sql statement.')
        except sqlalchemy.exc.OperationalError as e:
            logger.error(e)
            logger.error('Unable to connect to SQL.')
            raise e
        except Exception as e:
            logger.error(e)
            logger.error('Unable to connect to SQL.')
            raise e
