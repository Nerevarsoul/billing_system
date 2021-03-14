import importlib
import logging
import os

logger = logging.getLogger(__name__)


class Settings:

    def __init__(self):
        module = self.set_module()

        for setting_name in dir(module):
            setting_value = getattr(module, setting_name)
            if setting_name.isupper():
                setattr(self, setting_name, setting_value)

    @staticmethod
    def set_module():

        settings_module = os.getenv('SETTINGS_MODULE', 'app.settings.local')

        try:
            module = importlib.import_module(settings_module)
            logger.info('Using settings module: %s', settings_module)
        except ModuleNotFoundError:
            module = importlib.import_module('app.settings.base')
            logger.warning('Module %s not found. Using base.py settings module.', settings_module)

        return module


settings = Settings()
