from ..utilities import Utilities as utils
from .tests_sql import BASIC_TABLE_DATA_COLS, BASIC_TABLE_DATA_1
import pytest

class TestsUtilities:

    def test_utils_levels_dict_to_sql_string(self):
        levels = {'Brd':1, 'Drd': 2, 'Sor/Wiz': 3}
        levels_str = "Brd 1, Drd 2, Sor/Wiz 3"
        assert utils.levels_dict_to_sql_string(levels) == levels_str

    def test_utils_dict_to_sql_values_pair(self):
        test_dict = dict(BASIC_TABLE_DATA_COLS, BASIC_TABLE_DATA_1)
        test_dict_output = "(name,type,threat,elements) VALUES (Gore Magala,???,9,Frenzy)"
        assert utils.dict_to_sql_values_pair(test_dict) == test_dict_output

    def test_utils_parenthesized_list(self):
        ls = list(BASIC_TABLE_DATA_COLS, BASIC_TABLE_DATA_1)
        ls_output = "(name,type,threat,elements,Gore Magala,???,9,Frenzy)"
        assert utils.parenthesized_list(ls) == ls_output

    def test_utils_datetime_string(self):
        # not sure how to test this, since it depends on datetime.now()
        pass