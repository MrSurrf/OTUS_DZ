from dependency_injector import containers, providers
from src.plugins.plugin_manager import PluginManager
from src.plugins.RequestManager import RequestManager

class DIContainer(containers.DeclarativeContainer):
    
    
    # Создаем провайдер для RequestManager
    request_manager = providers.Singleton(
        RequestManager
    )
    
    # Создаем провайдер для PluginManager с зависимостью от RequestManager
    plugin_manager = providers.Singleton(
        PluginManager,
        request=request_manager
    ) 