from IRule import IRule


class Rule(IRule):

    def __init__(self):
        self.param = None
        self.name = None
        self.url = None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def get_param(self):
        return self.param

    def set_param(self, param):
        self.param = param

    def run(self, request_data):
        # Если параметры не заданы, это правило используется по умолчанию
        if self.get_param() is None:
            return True

        # Сверяем каждый параметр с данными запроса
        for key, value in self.param.items():
            if value not in str(request_data.values()):
                return False

        return True
