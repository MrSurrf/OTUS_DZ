import importlib
import os
import logging
import inspect
from handlers.plugins_interfaces import PluginInterface

logger = logging.getLogger(__name__)


class PluginManager:
    def __init__(self, plugin_folder):
        self.plugin_folder = plugin_folder
        self.plugins = []

    def load_plugins(self):
        """Загружает все плагины из указанной директории"""
        logger.info(f"Загрузка плагинов из директории: {self.plugin_folder}")

        try:
            for filename in os.listdir(self.plugin_folder):
                if filename.endswith('.py') and filename != 'plugins_interfaces.py' and not filename.startswith('__'):
                    self._load_plugin_from_file(filename)
        except Exception as e:
            logger.error(f"Ошибка при загрузке плагинов: {e}")

    def _load_plugin_from_file(self, filename):
        """Загружает плагин из указанного файла"""
        try:
            module_name = filename[:-3]  # Убираем расширение .py
            logger.info(f"Загрузка модуля: {module_name}")

            module = importlib.import_module(f"handlers.{module_name}")

            # Ищем все классы в модуле, которые являются подклассами PluginInterface
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (inspect.isclass(attr) and
                        issubclass(attr, PluginInterface) and
                        attr is not PluginInterface):
                    logger.info(f"Найден плагин: {attr.__name__}")
                    plugin_instance = attr()
                    self.plugins.append(plugin_instance)
                    logger.info(f"Плагин {plugin_instance.get_name()} успешно загружен")

        except Exception as e:
            logger.error(f"Ошибка при загрузке плагина из файла {filename}: {e}")

    def get_plugins(self):
        """Возвращает список загруженных плагинов"""
        return self.plugins

    def get_plugin_names(self):
        """Возвращает список имен загруженных плагинов"""
        return [plugin.get_name() for plugin in self.plugins]

