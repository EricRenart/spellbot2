from typing_extensions import Self
from sql import SQLManager
from utilities import Utilities as utils
import logging

class SDBLog:

    def _log_message(msg, level=logging.DEBUG, print_only=False, preamble=False):
        """
        Logs a message to logging module at the given log level, inserts it into the
        logging table, and optionally appends a preamble with the current date and time.
        :param msg: Message to log
        :param level: Log level to use
        :param print_only: if True, only prints out log message without adding it to log table
        :param preamble: Whether to append datetime to log message
        """

        # Add preamble to log message for output
        if preamble:
            to_logging_msg = f"[{utils.datetime_string()} SpellBot2] {msg}"
        else:
            to_logging_msg = msg
        
        # Log in logging module
        logging.log(to_logging_msg, level=level)
        
        # Insert log message into database
        if not print_only:
            SQLManager._add_log_message(msg, level=level)
    
    """
    Convenience functions
    """
    def critical(self, msg):
        self._log_message(msg, level=logging.CRITICAL)

    def error(self, msg):
        self._log_message(msg, level=logging.ERROR)
    
    def warning(self, msg):
        self._log_message(msg, level=logging.WARNING)
    
    def info(self, msg):
        self._log_message(msg, level=logging.INFO)
    
    def debug(self, msg):
        self._log_message(msg, level=logging.DEBUG)
    
    """
    Functions that retrieve data from logging db
    """
    def _get_last_raw(self, num_msgs=0):
        return SQLManager._query(f"SELECT * FROM spelldb2_log", fetch=True, fetch_rows=num_msgs)

    def get_last(self, num_msgs=0):
        """
        Gets the last n messages from the logging table.
        TODO: format output as string
        """
        log_msgs = self._get_last_raw(num_msgs=num_msgs)
        return log_msgs
