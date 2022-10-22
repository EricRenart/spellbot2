from configparser import ConfigParser
from typing_extensions import Self

class ConfigManager:

    def __init__(self, config_path='config.cfg'):
        self.config = ConfigParser()
        self.config.read_file(config_path)
    
    def get(self, section, value):
        """
        Gets the specified value from the specified section in the config file.
        :param section: Section of value to retrieve
        :param value: Value to retrieve
        :return: config file value
        """
        if not self.config.has_section(section):
            raise ValueError(f'Section {section} not found in config file')
        if self.config[section][value] is None:
            raise ValueError(f'Key {value} was not found in config file section {section}')
        return self.config[section][value]