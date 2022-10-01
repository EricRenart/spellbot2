import psycopg2
import config
import logging

TABLE_NAME_5 = '5espells'
TABLE_NAME_35 = '35espells'

class SQLManager:

    def __init__(self, connect=True):
        # Connection to pgsql database
        dbconfig = config.get_section('database')
        self.host = dbconfig.get('host')
        self.port = dbconfig.get('port')
        self.dbname = dbconfig.get('dbname')
        self.user = dbconfig.get('user')
        self.password = dbconfig.get('password')
        if connect:
            logging.info(f'Connecting to database {self.dbname}')
            self.connect()
    
    def connect(self):
        self.connection = psycopg2.connect(host=self.host, port=self.port, dbname=self.dbname,\
            username=self.user, password=self.password)
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        logging.info(f"Closing connection to {self.dbname}")
        self.connection.close()

    def _create_initial_tables(self):
        self.query(f"""CREATE TABLE {TABLE_NAME_35} (
            name varchar(50)
            description varchar(250)
            complete_description varchar(5000)
            components varchar(6)
            range int
            school varchar(15)
            casting_time varchar(10)
            target varchar(50)
            duration varchar()
        )""")
    
    def query(self, query_string, log=True, return_results=False):
        if log:
            logging.debug(f"""Executing query {query_string} on database {self.dbname}""")
        self.cursor.execute(query_string)
        if log:
            logging.debug(f"Query executed")
            rows = len(self.cursor.fetchall())
            logging.debug(f"Returned {rows} rows")
        if return_results:
            return self.cursor.fetchall()
    
    def initial_setup(self):
        logging.info('Setting up database')
        # Create initial database
        self.query(f"CREATE DATABASE {self.dbname}")

        # Create user and set permissions
        self.query(f"CREATE USER {self.user}")
        self.query(f"""GRANT SELECT, INSERT, UPDATE, DELETE ON {self.dbname} TO USER {self.user}""")
