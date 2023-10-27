from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.components.settings_manager_component import SettingsManagerComponent
from feature_extraction_server.core.settings import EnumSetting, StringSetting
from feature_extraction_server.core.log_server import LogServer

class LogServerComponent(Component):
    
    @staticmethod
    def _init():
        settings_manager = SettingsManagerComponent.get()
        log_level_setting = EnumSetting("LOG_LEVEL", "INFO", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "The log level.")
        log_path_setting = StringSetting("LOG_PATH", "logs/log.txt", "The path to the log file.")
        settings_manager.add_setting(log_level_setting)
        settings_manager.add_setting(log_path_setting)
        log_server = LogServer(log_level_setting.get(), log_path_setting.get())
        
        log_server.start_server()
        
        return log_server