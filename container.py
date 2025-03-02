from dependency_injector import containers, providers
from Rules_manadger import RulesManager
from Plugin_manager import PluginManager
from request_manager import RequestManager

class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    rules_manager = providers.Singleton(RulesManager, rules_file=config.rules_file)
    plugin_manager = providers.Singleton(PluginManager, plugin_folder=config.handlers_dir)
    request_manager = providers.Singleton(RequestManager)

    @staticmethod
    def _get_redirect_url(rules_manager, plugin_manager, request_data):
        rules = rules_manager.get_rules()
        print(rules)
        for rule in rules.items():
            print(rule)
            for plugin in plugin_manager.get_plugins():
                result = plugin.run(rule, request_data)
                if result:
                    return result
        return 'https://default.com'

    redirect_factory = providers.Factory(
        lambda rules_manager, plugin_manager:
        lambda request_data: AppContainer._get_redirect_url(rules_manager, plugin_manager, request_data)
    )

