from ast import arg
from keyword import kwlist
import psycopg2
import config
import logging
from utilities import Utilities as utils

TABLE_COLUMNS = {'name': 'varchar(50)',
                'description': 'varchar(250)',
                'complete_description': 'varchar(5000)',
                'components': 'varchar(75)',
                'range': 'int',
                'school': 'varchar(15)',
                'casting_time': 'varchar(10)',
                'target': 'varchar(50)',
                'duration': 'varchar(15)',
                'source': 'varchar(50)',
                'page': 'int'}

class SQLManager:

    def __init__(self, connect=True, edition='3.5'):
        # Connection to pgsql database
        dbconfig = config.get_section('database')
        self.host = dbconfig.get('host')
        self.port = dbconfig.get('port')
        self.dbname = dbconfig.get('dbname')
        self.user = dbconfig.get('user')
        self.password = dbconfig.get('password')
        self.schema = dbconfig.get('schema')
        self.edition = edition
        self.master_table_name = f"spellbot2_{self.user}_{self.edition}e"
        self.tables = [self.master_table_name]
        if connect:
            self.connect()
    
    def _add_table(self, tablename: str, columns: dict, schema=None, return_results=False):
        if schema == None:
            schema = self.schema
        qry = f"""CREATE TABLE {schema}.{tablename}\n"""
        for col in columns.keys():
            # column: dtype
            qry += f"{col}: {columns.get(col)},\n"
        qry += ')'
        self.query(qry, return_results=return_results)
    
    def _insert_to_table(self, tablename: str, values: dict, schema=None, return_results=False):
        if schema == None:
            schema == self.schema
        qry = f"""INSERT INTO {schema}.{tablename} {utils.dict_to_sql_values_pair(values)}"""
        self.query(qry, return_results=return_results)
    
    def _drop_table(self, tablename: str, schema=None, cascade=False, return_results=False):
        if schema == None:
            schema = self.schema
        qry = f"""DROP TABLE {schema}.{tablename}"""
        if cascade:
            qry += " CASCADE"
        self.query(qry, return_results=return_results)

    def connect(self):
        logging.info(f'Connecting to database {self.dbname}...')
        self.connection = psycopg2.connect(host=self.host, port=self.port, dbname=self.dbname,\
            username=self.user, password=self.password)
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        logging.info(f"Closing connection to {self.dbname}")
        self.connection.close()
    
    def add_spell(self, name: str, levels: dict, description: str, long_description: str,
    casting_time: str, duration: str, range: str, components: str, effect: str, save: str, src: str, src_pg: int,
    return_results=False):
        levels_str = utils.levels_dict_to_sql_string(levels)
        data_dict = dict(TABLE_COLUMNS.keys(),
                        [name,levels_str,description,long_description,
                        casting_time,duration,range,components,effect,save,src,src_pg])
        self._insert_to_table(self.master_table_name, values=data_dict, schema=self.schema, return_results=return_results)

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
        self.query(f"""GRANT ALL PRIVILEGES ON {self.dbname} TO {self.user}""")

        # Add initial table
        logging.info("Creating master table")
        self._add_table(self.master_table_name, columns=TABLE_COLUMNS, schema=self.schema)