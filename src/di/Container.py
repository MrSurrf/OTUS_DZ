from src.rules.RuleManager import RulesManager
from src.rules.RuleBuilder import RuleBuilder
from src.plugins.plugin_manager import PluginManager

from src.di.containers import DIContainer


class Container:

    def __init__(self, request_data, app):
      
        self.manager = RulesManager("rule.json")
        self.builder = RuleBuilder()
        self.rules_list = self.manager.get_rules()
        self.list = []
        self.redirect_url = ''
        self.is_ready = False        

        #app.container.plugin_manager()
        current_manager = PluginManager(request_data)       
        current_manager.plugin_element_list()

        '''Проходим по сырому массиву правил от RulesManager
         и составляем на его основе массив полноценных сущностей типа Rule'''
        for yet_another_rule in self.rules_list:
            self.prepared_rule = self.builder.for_name(yet_another_rule["name"])\
                             .for_url(yet_another_rule['redirect'])\
                             .for_params(yet_another_rule['params'])\
                             .for_plugin_manager(current_manager).build()
            self.list.append(self.prepared_rule)
            self.builder.reset()

        '''Проходим по полученному на прошлом шаге массиву и находим Rule, который выполняется'''
        for yet_another_element in self.list:
            if yet_another_element.run(request_data):
                self.redirect_url = yet_another_element.get_url()
                break

        self.is_ready = True

    def get_is_ready(self):
        return self.is_ready

    def get_redirect_url(self):
        return self.redirect_url 