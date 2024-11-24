from typing import Any
import simple_plugin_manager.plugin as plugin
from simple_plugin_manager.service_manager import ServiceManager
from simple_plugin_manager.exceptions import MissingConfigurationException
from simple_plugin_manager.settings import Setting, FlagSetting
from simple_plugin_manager.plugin import register_plugin

from tabulate import tabulate

class Config(ServiceManager.Plugin):
    class Plugin(plugin.Plugin):
        settings = []
        
        def __init__(self):
            vars = {}
            for setting in self.settings:
                try:
                    vars[setting.upper_name] = setting.get()
                except MissingConfigurationException:
                    pass
            self.__dict__.update(vars)
            
        def __init_subclass__(cls) -> None:
            
            @register_plugin
            class ServicePlugin(ServiceManager.Plugin):
                service_type = cls
                def build_service(self):
                    return cls()
            
            cls.ServicePlugin = ServicePlugin
        
        def __setattr__(self, __name: str, __value: Any) -> None:
            raise AttributeError("Config is immutable")

    def __init__(self):
        vars = {}
        self.settings = self._gather_all_settings()
        self.help_setting = FlagSetting(name='help', description='Prints the help message.')
        self.settings.append(self.help_setting)
        for setting in self.settings:
            try:
                vars[setting.upper_name] = setting.get()
            except MissingConfigurationException:
                pass
        self.__dict__.update(vars)
    
    def _format_help_message(self):
        table = []
        table.append(["Name", "Command Line Argument" ,"Description"])
        for setting in self.settings:
            table.append([setting.upper_name, f"--{setting.lower_name_dash}", setting.description])
        
        return tabulate(table, headers="firstrow", tablefmt="grid")
    
    def _gather_all_settings(self):
        settings = []
        for config_plugin in self.Plugin.get_implementations():
            for setting in config_plugin.settings:
                if not isinstance(setting, Setting):
                    raise ValueError(f"Invalid setting: {setting}. Must be an instance of Setting")
                if setting.upper_name in [s.upper_name for s in settings]:
                    raise ValueError(f"Setting {setting.upper_name} already exists")
                settings.append(setting)
        return settings
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        raise AttributeError("Config is immutable")
    
    
    

class ConfigProvider(ServiceManager.Plugin):
    service_type = Config
    def build_service(self):
        return Config()