
from abc import ABC, abstractmethod

class PluginInterface(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def run(self, rule, request_data):
        pass





# class PluginInterface:
#     def get_name(self): # плагин возвращает свое имя
#         pass
#     def run(self): # плагин реализовывает метод run
#         pass