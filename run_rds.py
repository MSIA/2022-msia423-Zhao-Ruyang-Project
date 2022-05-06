import logging.config
import os

from src.rds_util import RdsUtil

# Create a logger and specify the configurations
logging.config.fileConfig('./config/logging/local.conf')
logger = logging.getLogger('run_rds.py')

# Get the engine string from environment variable
ENGINE_STRING = os.getenv("SQLALCHEMY_DATABASE_URI")
# Instantiate RdsUtil to connect to sql
rds_util = RdsUtil(ENGINE_STRING)

# Drop the database if it already exists
try:
    rds_util.exec_sql('DROP DATABASE IF EXISTS test;')
except Exception as e:
    logger.error('Unable to DROP the database.')
    raise e
else:
    logger.info('DROP the database successfully.')

# Create the database
try:
    rds_util.exec_sql('CREATE DATABASE test;')
except Exception as e:
    logger.error('Unable to CREATE the database.')
    raise e
else:
    logger.info('CREATE the database successfully.')

# Use the database
rds_util.exec_sql('USE test;')

# SQL statement to create the UserInputs table
sql_statement = """
            CREATE TABLE UserInputs (
                cUserID int(11),
                DepartureDate date,
                DepartureTime time,
                Source varchar(255),
                Destination varchar(255),
                Stops int(11),
                TotalTime int(11),
                FlightNumber varchar(255)
            );
            """

# Execute the table generation statement
try:
    rds_util.exec_sql(sql_statement)
except Exception as e:
    logger.error('Unable to CREATE the table successfully')
    raise e
else:
    logger.info('CREATE the table successfully.')


# try:
#     engine = create_engine('mysql+pymysql://rzx9163:Aws1998!@nw-msia423-rzx9163.ctarvegaqgdp.us-east-1.rds.amazonaws.com:3306/msia423_db')
# except sqlalchemy.exc.NoSuchModuleError as e:
#     logger.error(e)
#     logger.error('Unable to connect to the sql engine.')
#     raise e
# except Exception as e:
#     logger.error(e)
#     logger.error('Unable to connect to the sql engine.')
#     raise e
# try:
#     with engine.connect() as con:
#         try:
#             con.execute('DROP DATABASE IF EXISTS test;')
#             con.execute('CREATE DATABASE test;')
#         except sqlalchemy.exc.ProgrammingError as e:
#             logger.error('Unable to create the database.')
#
#         try:
#             con.execute('USE test;')
#             con.execute("""
#             CREATE TABLE UserInputs (
#                 cUserID int(11),
#                 DepartureDate date,
#                 DepartureTime time,
#                 Source varchar(255),
#                 Destination varchar(255),
#                 Stops int(11),
#                 TotalTime int(11),
#                 FlightNumber varchar(255)
#             );
#             """
#                         )
#         except sqlalchemy.exc.ProgrammingError as e:
#             logger.error('Unable to create the table.')
# except sqlalchemy.exc.OperationalError as e:
#     logger.error(e)
#     logger.error('Error processing the sql statement.')
#     raise e
