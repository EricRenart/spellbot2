from .log import SB2Log
from .sql import SQLManager as sql
from .config import ConfigManager as config

bot = Commands.Bot(command_prefix='!')

class DiscordBot:
    def __init__(self, cfg_path='config.cfg') -> None:
        # Initialize app components
        self.config = config.ConfigManager(config_path=cfg_path)
        self.db = sql.SQLManager(connect=True)


    @bot.command(name='spell', description='Looks up given spell by name and displays info')
    def cmd_spell(self, ctx, spell_name):
        """
        Looks up given spell name in database and displays its info.
        """
        pass

    @bot.command(name='edition', description='Changes D&D edition between 3.5e and 5e')
    def cmd_edition(self):
        """
        Changes mode of the bot between 3.5e and 5e.
        TODO: add support for Changeling?
        """
        pass

    @bot.command(name='search', description='Search for a spell by school, level or class')
    def cmd_search(self, ctx, *args):
        """
        Queries the spell database to search for spells
        """
        pass

    @bot.command(name='dbmode', description='Changes database mode of the bot')
    def cmd_config(self, ctx, arg):
        """
        Changes database mode from
        """

        pass