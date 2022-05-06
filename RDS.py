import logging.config
from sqlalchemy import create_engine


# Create a logger and specify the configurations
logging.config.fileConfig('./config/logging/local.conf')
logger = logging.getLogger('RDS.py')

ENGINE_STRING = "mysql+pymysql://rzx9163:Aws1998!@nw-msia423-rzx9163.ctarvegaqgdp.us-east-1.rds.amazonaws.com:3306/msia423_db"
engine = create_engine(ENGINE_STRING)

try:
    with engine.connect() as con:
        con.execute('DROP DATABASE IF EXISTS test;')
        con.execute('CREATE DATABASE test;')
        con.execute('USE test;')
        con.execute("""
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
                    )
except Exception as e:
    raise e