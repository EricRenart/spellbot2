from configparser import ConfigParser

class ConfigManager:

    def __init__(self, config_path='config.cfg'):
        self.read_configfile(config_path)

    def read_configfile(self, config_path):
        self.config = ConfigParser.read_file(config_path)
    
    def get_section(self, name):
        if not self.config.has_section(name):
            raise ValueError(f'Section {name} not found in configfile')