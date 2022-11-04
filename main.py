import config
import sql
from log import SB2Log
from discord_bot import DiscordBot
import logging

class SpellBot2:
    def __init__(self, conf_file='config.cfg'):
        logging.basicConfig(level=logging.DEBUG)
        logging.info('Welcome to SpellBot 2.')
