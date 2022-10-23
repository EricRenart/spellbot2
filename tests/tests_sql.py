from ..sql import SQLManager
from ..config import ConfigManager
from os import path
import pytest

TEST_CONFIG_FILENAME_EXT = 'config_test.cfg'
TEST_SQLITE_FILENAME = 'spelldb2_test.sqlite'
TEST_SQLITE_LOG_FILENAME = 'spelldb2_test_log.sqlite'
TEST_CONFIG_PATH = path.join(path.dirname('tests'), TEST_CONFIG_FILENAME_EXT)

BASIC_TABLE_NAME = 'spelldb2_test_monsters'
BASIC_TABLE_DATA_COLS = ['name','type','threat','elements']
BASIC_TABLE_DATA_1 = ['Gore Magala', '???', 9, ['Frenzy']]
BASIC_TABLE_DATA_2 = ['Narwa the Allmother', 'Elder Dragon', 10, ['Thunder','Dragon']]
BASIC_TABLE_DATA_3 = ['Alatreon', 'Elder Dragon', 10, ['Fire','Water','Thunder','Ice','Dragon']]
BASIC_TABLE_DATA_4 = ['Barioth', 'Psuedo-flying Wyvern', 5, ['Ice']]
BASIC_TABLE_DATA_5 = ['Equal Dragon Weapon', 'Construct', 10, ['Fire','Water','Thunder','Ice','Dragon']]

"""
Note: This does not test the log table, see tests_logging.py
"""
class TestsSQLManager:

    @classmethod
    def setup(cls):
        """
        Sets up the SQLManager instance to test.
        """
        cls.cm = ConfigManager(config_path=TEST_CONFIG_FILENAME_EXT)
        cls.sqlm = SQLManager(connect=False, setup=False)

    def test_sqlm_connect_disconnect(self):
        assert self.sqlm.connected == False
        self.sqlm.connect()
        assert self.sqlm.connected == True
        self.sqlm.disconnect()
        assert self.sqlm.connected == False

        # make sure to connect to run following tests
        self.sqlm.connect()
        assert self.sqlm.connected == True

    def test_sqlm_create_basic_table(self):
        # assert test table hasn't been created yet
        pass

    def test_sqlm_drop_basic_table(self):
        pass

    def test_sqlm_clear_basic_table(self):
        pass

    def test_sqlm_insert_basic_table(self):
        pass

    def test_sqlm_commit_queries_basic_table(self):
        pass

    def test_sqlm_create_master_table(self):
        pass

    def test_sqlm_drop_master_table(self):
        pass

    def test_sqlm_clear_master_table(self):
        pass

    def test_sqlm_insert_master_table(self):
        pass

    def test_sqlm_commit_queries_master_table(self):
        pass
    
    def test_sqlm_query_time(self):
        pass

    @classmethod
    def teardown(cls):
        cls.sqlm.db.close()