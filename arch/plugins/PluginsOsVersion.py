from IPlugins import IPlugins


class PluginOS(IPlugins):

    def __init__(self):
        self.needs_data = True
        self.name = "Версия операционной системы"
        self.keys = 'os_version'
        self.data = {}

    def get_name(self):
        return self.name

    def get_keys(self):
        return self.keys

    def get_data(self, request):
        self.data = request

    def does_need_data(self):
        return self.needs_data

    def run_plugin(self, rule_value):
        print(self.data[self.keys])
        return self.data[self.keys] == rule_value



