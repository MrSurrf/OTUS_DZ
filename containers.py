from dependency_injector import containers, providers
from PluginManager import PluginManager
from RequestManager import RequestManager

class DIContainer(containers.DeclarativeContainer):
    # Конфигурация, если потребуется
    config = providers.Configuration()
    
    # Создаем провайдер для RequestManager
    request_manager = providers.Singleton(
        RequestManager
    )
    
    # Создаем провайдер для PluginManager с зависимостью от RequestManager
    plugin_manager = providers.Singleton(
        PluginManager,
        request=request_manager
    ) 