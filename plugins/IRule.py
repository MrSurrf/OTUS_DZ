from abc import abstractmethod


class IRule:

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def set_name(self, name):
        pass

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def set_url(self, url):
        pass

    @abstractmethod
    def get_param(self):
        pass

    @abstractmethod
    def set_param(self, param):
        pass

    @abstractmethod
    def run(self, request_data):
        pass
