from datetime import datetime
import sqlite3
from typing_extensions import Self
import config
from log import SB2Log
import logging
import datetime
from utilities import Utilities as utils

# list of column names for database tables
TABLE_COLUMNS = ['name','description','complete_description','components','range',
'school','casting_time','target','duration','source','page']
LOG_TABLE_COLUMNS = ['datetime','level','message']
class SQLManager:

    """
    SQLManager
    This class manages SQLite3 database instances for spelldb2
    """

    def __init__(self,  db_filename=None, connect=True, setup=False, edition='5'):
        """
        Create a new instance of this SQL manager.
        :param db_filename: Name of .sqlite file to be created for database. If None, use default name. Default None.
        :param connect: Whether to connect to database upon creation. Default True.
        :param edition: D&D edition to read in spells for. Default 5. This will pull in spells from
        the relevant sources based on edition.
        Available values: 3.5, 5
        :param setup: Whether to load spell data and set up tables upon creation. Default True.
        :return: SQLManager instance
        """
        self.edition = config.ConfigManager.get('spells','default_edition')
        if edition != '3.5' or '5':
            raise ValueError('D&D edition must be 3.5 or 5 in config file.')
        self.db_filename = f"spellbot2_{self.edition}e.sqlite"
        self.master_table_name = self.db_filename.rstrip('.sqlite')
        self.log_table_name = "spellbot2_log"
        self.tables = [self.master_table_name, self.log_table_name]
        self.pending_transactions = list()
        self.cursor = None
        self.connected = False
        if connect:
            self.connect(db_filename=db_filename)
        if setup:
            self.initial_setup()

    def __len__(self):
        """
        Returns the number of rows in the db.
        """
        all_data = self._query(f"SELECT * FROM {self.master_table_name}", fetch_results=True)
        return len(all_data)
    
    def connect(self, db_filename=None):
        """
        Opens connection to the SQLite3 database.
        :param db_filename: .db file to connect to. If None, uses default filename. Default None.
        """

        # use default filename if None
        if db_filename == None:
            db_filename = self.db_filename

        SB2Log.info(f'Initiating SQLite3 connection to {db_filename}')
        self.db = sqlite3.connect(db_filename)
        self.cursor = self.db.cursor()
        self.connected = True

        # set new db filename in SQLManager if specified
        if db_filename != None:
            self.db_filename = db_filename

        SB2Log.info(f'Connection to {self.db_filename} established.')
    
    def disconnect(self):
        """
        Closes connection to the SQLite3 database.
        """
        SB2Log.info(f'Closing sqlite3 connection to {self.db_filename}')
        self.db.close()
        self.cursor = None
        self.connected = False
        SB2Log.info(f'Connection closed.')
    
    def _query(self, qry, commit=False, fetch=True, fetch_rows=0, timeme=True):
        """
        Runs a query on the SQLite3 database.
        :param qry: SQL query string to run
        :param commit: Whether to commit query
        :param fetch: Whether to return results after running query. Default True.
        :param fetch_rows: How many rows of data to return if fetch=True. If 0, return all rows. Default 0.
        :param timeme: Whether to log execution time of query
        :return: data rows, if fetch=True 
        """
        t1, t2, dt = None
        SB2Log.debug(f"Executing SQL3 query on {self.db_filename}:\n{qry}\n")

        if self.connected:

            # mark start time
            if timeme:
                t1 = datetime.datetime.now()
            
            # query
            self.cursor.execute(qry)

            # mark end time and calculate execution time
            if timeme:
                t2 = datetime.datetime.now()
                dt = t2 - t1
                SB2Log.debug(f"Query took {str(dt)} ms.")

            # add to pending queries list
            self.pending_transactions.append(qry)

            # commit pending transactions to DB
            if commit:
                self.commit()
            
            # get query results
            if fetch:
                if fetch_rows == 1:
                    # return first row only
                    return self.cursor.fetchone()
                elif fetch_rows > 1:
                    # fetch the number of rows specified by fetch_rows param
                    return self.cursor.fetchmany(fetch_rows)
                else:
                    # return all rows
                    return self.cursor.fetchall()
        
        else:
            # raise ConnectionError if connection isn't open
            err_str = 'Cannot read in data from a closed connection'
            SB2Log.error(err_str)
            raise ConnectionError(err_str)
    
    def commit(self):
        """
        Commits all transactions in pending_transactions to db (writes to disk)
        """
        SB2Log.info(f"Committing {len(self.pending_transactions)} pending transactions to database.")
        self.db.commit()
        self.pending_transactions = list()

    def initial_setup(self):
        """
        Sets up initial database tables and columns.
        """
        self._setup_logging_table()
        self._setup_master_table()

    def _setup_master_table(self):
        """
        Sets up master spell table.
        Make sure to call _setup_logging_table() before calling this!
        """
        # TODO: check in code if _setup_logging_table() has been called and throw error if it hasn't
        SB2Log.info("Setting up master spell table")
        self._query(f"CREATE TABLE {self.master_table_name} {utils.parenthesized_list(TABLE_COLUMNS)}")
        SB2Log.info("Master spell table created.")
    
    def _setup_logging_table(self):
        """
        Sets up table for logging.
        This function must be called before _setup_master_table().
        """
        # can't log to table yet as it isn't set up
        SB2Log.info("Setting up logging table", print_only=True)
        self._query(f"CREATE TABLE {self.log_table_name} {utils.parenthesized_list(LOG_TABLE_COLUMNS)}")
        SB2Log.info("Logging table created")

    def _add_log_message(self, msg, level):
        """
        Adds a log message to the logging table with the given log level.
        """
        msg_dict = {'datetime': datetime.datetime.now(),
                    'level': level,
                    'message': msg}
        valspair = utils.dict_to_sql_values_pair(msg_dict)
        self._query(f"INSERT INTO {self.log_table_name} {valspair}")
        
    def _clear_logging_table(self):
        """
        Drops logging table and re-creates it.
        """
        self._query(f"DROP TABLE {self.log_table_name}")
        self._setup_logging_table()