from abc import abstractmethod


class IPlugins:

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_keys(self):
        pass

    @abstractmethod
    def does_need_data(self):
        pass

    @abstractmethod
    def get_data(self, data):
        pass

    @abstractmethod
    def run_plugin(self, rule_value):
        pass
