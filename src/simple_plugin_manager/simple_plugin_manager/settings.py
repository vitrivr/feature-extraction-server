
from argparse import ArgumentParser
from decouple import config, UndefinedValueError

import abc
from simple_plugin_manager.exceptions import InvalidConfigurationException, MissingConfigurationException
import logging

logger = logging.getLogger(__name__)

class NoValue:
    pass

class Setting(abc.ABC):
    def __init__(self, name, default, description):
        self.lower_name_dash = name.lower().replace('_', '-')
        self.lower_name_underscore = self.lower_name_dash.replace('-', '_')
        self.upper_name = self.lower_name_underscore.upper()
        self.default = default
        self.description = description
    
    def get(self):
        value = self.get_from_args()
        if value is not NoValue and self.check(value):
            return value
        value = self.get_from_env()
        if value is not NoValue and self.check(value):
            return value
        value = self.default
        if value is not NoValue and self.check(value):
            return value
        if value is NoValue:
            error_msg = f"Missing {self.upper_name}"
            logger.warning(error_msg)
            raise MissingConfigurationException(error_msg)
        
        error_msg = f"Invalid {self.upper_name}: {value}"
        logger.error(error_msg)
        raise InvalidConfigurationException(error_msg)
    
    def _get_from_args(self, type):
        ap = ArgumentParser(add_help=False)
        ap.add_argument(f'--{self.lower_name_dash}', dest=self.upper_name, type=type)
        args, unknown = ap.parse_known_args()
        if self.upper_name in vars(args):
            return vars(args)[self.upper_name]
        return NoValue
    
    def get_from_env(self):
        try:
            return config(self.upper_name)
        except UndefinedValueError:
            return NoValue
    
    @abc.abstractmethod
    def get_from_args(self):
        pass
    
    @abc.abstractmethod
    def check(self, value):
        pass

class EnumSetting(Setting):
    def __init__(self, name, default, valid_values, description, describe_valid_values=True):
        if describe_valid_values:
            description = description + " Must be one of " + str(valid_values)
        super().__init__(name, default, description)
        self.valid_values = valid_values
    
    def get_from_args(self):
        return self._get_from_args(str)
    
    def check(self, value):
        return value in self.valid_values

class FlagSetting(Setting):
    def __init__(self, name, description):
        super().__init__(name, False, description)
    
    def get_from_args(self):
        ap = ArgumentParser(add_help=False)
        ap.add_argument(f'--{self.lower_name_dash}', dest=self.upper_name, action='store_true')
        args, unknown = ap.parse_known_args()
        if self.upper_name in vars(args):
            if vars(args)[self.upper_name]:
                return True
        return NoValue
    
    def check(self, value):
        return type(value) is bool

class StringListSetting(Setting):
    
    def get_from_env(self):
        return [item.strip() for item in super().get_from_env().split(',')]
    
    def get_from_args(self):
        return [item.strip() for item in self._get_from_args(str).split(',')]
    
    def check(self, value):
        return all([item is str for item in value])

class IntegerSetting(Setting):
    
    def get_from_env(self):
        raw = super().get_from_env()
        if raw is NoValue:
            return raw
        try:
            return int(raw)
        except ValueError as e:
            raise InvalidConfigurationException(f"Invalid {self.upper_name}: {raw}") from e
    
    def get_from_args(self):
        return self._get_from_args(int)
    
    def check(self, value):
        return type(value) is int

class FloatSetting(Setting):
    
    def get_from_env(self):
        raw = super().get_from_env()
        if raw is NoValue:
            return raw
        try:
            return float(raw)
        except ValueError as e:
            raise InvalidConfigurationException(f"Invalid {self.upper_name}: {raw}") from e
    
    def get_from_args(self):
        return self._get_from_args(float)
    
    def check(self, value):
        return type(value) is float

class StringSetting(Setting):
    
    def get_from_args(self):
        return self._get_from_args(str)
    
    def check(self, value):
        return type(value) is str