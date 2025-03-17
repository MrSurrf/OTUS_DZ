from src.rules.Rule import Rule


class RuleBuilder:

    def __init__(self):
        self.rule = Rule()

    def reset(self):
        self.rule = Rule()
        return self

    def for_name(self, name):
        self.rule.set_name(name)
        return self

    def for_url(self, url):
        self.rule.set_url(url)
        return self

    def for_param(self, key, value):
        params = self.rule.get_param()
        params[key] = value
        self.rule.set_param(params)
        return self

    def for_params(self, params):
        self.rule.set_param(params)
        return self

    def for_plugin_manager(self, manager):
        self.rule.set_plugin_manager(manager)
        return self
        
    def build(self):
        if not self.rule.get_url():
            raise ValueError("Url перенаправления обязателен")
        return self.rule 