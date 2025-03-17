import importlib.util
import inspect
import os
from src.plugins.IPlugins import IPlugins

class PluginManager:

    def __init__(self, request):
        self.plugin_folder = './src/plugins/checkers'
        self.plugins_dict = {}
        self.request_manage = request

    """Загружает все плагины из указанной директории"""
    def plugin_element_list(self):
        
        try:
            for filename in os.listdir(self.plugin_folder):
                if filename.endswith('.py'):
                    self._load_plugin_from_file(filename)
        except Exception as e:
            print(f"Ошибка загрузки плагинов: {e}")                                                                 # FIX!!!!!!!
        print("Финальный список плагинов в словаре:")
        for key, plugin in self.plugins_dict.items():
            print(f"Ключ: {key}, Плагин: {plugin.get_name()}")

        

    def _load_plugin_from_file(self, filename):
        """Загружает плагин из указанного файла"""
        try:
            module_name = filename[:-3]  

            file_path = os.path.join(self.plugin_folder, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)

            if spec is None:
                print(f"Не удалось создать спецификацию для {file_path}")
                return

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Ищем все классы в модуле, которые являются подклассами PluginInterface
            for attr_name in dir(module):

                attr = getattr(module, attr_name)
                if (inspect.isclass(attr) and
                        issubclass(attr, IPlugins) and
                        attr is not IPlugins):                    
                    plugin_instance = attr()
                    if plugin_instance.does_need_data():
                        plugin_instance.get_data(self.request_manage)

                    self.plugins_dict[plugin_instance.get_keys()] = plugin_instance
                    print(f"Плагин {plugin_instance.get_name()} успешно загружен")
        except Exception as e:
            print(f"Ошибка загрузки плагина {filename}: {e}")


    def get_value(self, key, rule_value):
        print(f"Вызов get_value с ключом: {key}")
        print(self.plugins_dict[key].run_plugin(rule_value))
        return self.plugins_dict[key].run_plugin(rule_value)

    def get_plugin_names(self):
        """Возвращает список имен доступных плагинов"""
        # Если плагины еще не загружены, загружаем их
        if not self.plugins_dict:
            self.plugin_element_list()

        # Возвращаем имена плагинов
        return [plugin.get_name() for plugin in self.plugins_dict.values()]

    def get_plugin_keys_and_names(self):
        """Возвращает словарь с ключами и именами плагинов"""
        # Если плагины еще не загружены, загружаем их
        if not self.plugins_dict:
            self.plugin_element_list()

        # Создаем словарь {ключ: имя}
        result = {}
        for key, plugin in self.plugins_dict.items():
            result[key] = plugin.get_name()

        return result 