from .log import SB2Log
bot = Commands.Bot(command_prefix='!')

class DiscordBot:
    def __init__(self, edition='5') -> None:
        if edition == '3.5' or edition == '5':
            self.edition = edition
        else:
            # use 5e as default edition and warn user
            SB2Log.warning(f"Unrecognized edition {edition}. I currently support D&D 3.5e and 5e. Setting to 5th edition as default.")
            self.edition = '5'

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