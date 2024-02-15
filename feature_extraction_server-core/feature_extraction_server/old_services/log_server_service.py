from injector import provider, Module, singleton
from feature_extraction_server.core.settings import EnumSetting, StringSetting
from feature_extraction_server.core.log_server import LogServer
from feature_extraction_server.core.settings import SettingsManager
from feature_extraction_server.services.locator_service import Locator
import multiprocessing as mp

class LogServerService(Module):
    
    @singleton
    @provider
    def start_log_server(self, settings_manager: SettingsManager, locator : Locator, mp_manager : mp.Manager) -> LogServer:
        log_level_setting = EnumSetting("LOG_LEVEL", "INFO", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "The log level.")
        log_path_setting = StringSetting("LOG_PATH", "logs/log.txt", "The path to the log file.")
        settings_manager.add_setting(log_level_setting)
        settings_manager.add_setting(log_path_setting)
        log_server = LogServer(log_level_setting.get(), log_path_setting.get(), mp_manager=mp_manager)
        
        log_server.start_server()
        
        locator.register_instance(LogServer, log_server)
        
        return log_server