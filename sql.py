import sqlite3
import config
import logging
from utilities import Utilities as utils

TABLE_COLUMNS = ['name','description','complete_description','components','range',
'school','casting_time','target','duration','source','page']
class SQLManager:

    """
    SQLManager
    This class manages SQLite3 database instances for spelldb2
    """

    def __init__(self, connect=True, setup=False, edition='5'):
        """
        Create a new instance of this SQL manager.
        :param connect: Whether to connect to database upon creation. Default True.
        :param edition: D&D edition to read in spells for. Default 5. This will pull in spells from
        the relevant sources based on edition.
        Available values: 3.5, 5
        :param setup: Whether to load spell data and set up tables upon creation. Default True.
        :return: SQLManager instance
        """
        self.edition = config.ConfigManager.get_section('spells').get('default_edition')
        if edition != '3.5' or '5':
            raise ValueError('D&D edition must be 3.5 or 5 in config file.')
        self.db_filename = f"spellbot2_{self.edition}e.db"
        self.master_table_name = self.db_filename.rstrip('.db')
        self.tables = [self.master_table_name]
        self.pending_queries = []
        self.cursor = None
        if connect:
            self.db = sqlite3.connect(self.db_filename)
            self.cursor = self.db.cursor()

    def __len__(self):
        """
        Returns the number of rows in the db.
        """
        all_data = self._query(f"SELECT * FROM {self.master_table_name}", fetch_results=True)
        return len(all_data)
    
    def _query(self, qry, commit=False, fetch=True, fetch_rows=0):
        """
        Runs a query on the db
        :param qry: SQL query string to run
        :param commit: Whether to commit query
        :param fetch: Whether to return results after running query. Default True.
        :param fetch_rows: How many rows of data to return if fetch=True. If 0, return all rows. Default 0.
        :return: data rows, if fetch=True 
        """
        # execute query
        logging.info(f"Executing SQL3 query on {self.db_filename}:\n{qry}\n")
        self.cursor.execute(qry)

        # add to pending queries list
        self.pending_queries.append(qry)

        # commit pending transactions to DB
        if commit:
            logging.info(f'Committing {len(self.pending_queries)} queries to {self.db_filename}')
            self.db.commit()
        
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
    
    def _setup_columns(self):
        """
        Sets up initial database tables and columns.
        """