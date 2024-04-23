from typing import Any
from tabulate import tabulate
from simple_plugin_manager.exceptions import MissingConfigurationException

from simple_plugin_manager.service import Service
from simple_plugin_manager.settings import Setting, FlagSetting
import sys
 
import logging 
logger = logging.getLogger(__name__)

class SettingsManager(Service):
    def __init__(self, help=False):
        self.settings = []
        self.help = help
    
    def add_setting(self, setting: Setting):
        if not isinstance(setting, Setting):
            raise ValueError(f"Invalid setting: {setting}. Must be an instance of Setting")
        if setting.upper_name in [s.upper_name for s in self.settings]:
            raise ValueError(f"Setting {setting.upper_name} already exists")
        self.settings.append(setting)
    
    def format_help(self):
        table = []
        table.append(["Name", "Command Line Argument" ,"Description"])
        for setting in self.settings:
            table.append([setting.upper_name, f"--{setting.lower_name_dash}", setting.description])
            
        return tabulate(table, headers="firstrow", tablefmt="grid")
    
    def get_config(self):
        conf_vars = {}
        for setting in self.settings:
            try:
                conf_vars[setting.upper_name] = setting.get()
            except MissingConfigurationException:
                pass
        return Config(conf_vars)
    
    def show_help(self):
        if self.help:
            print(self.format_help())
            sys.exit(0)
    
    @staticmethod
    def initialize_service():
        helpsetting = FlagSetting("help", "Show this help message")
        sm = SettingsManager(helpsetting.get())
        sm.add_setting(helpsetting)
        return sm
    

class Config:
    def __init__(self, vars):
        self.__dict__.update(vars)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        raise AttributeError("Config is immutable")