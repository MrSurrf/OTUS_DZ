class Rule:
    def __init__(self):
        self.name = None
        self.url = None
        self.param = {}
        self.plugin_manager = None

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

    def set_plugin_manager(self, manager):
        self.plugin_manager = manager

    def run(self, request_data):
        # Если параметры не заданы, это правило используется по умолчанию
        if self.get_param() is None:
            return True

        # Сверяем каждый параметр с данными запроса
        for key, value in self.param.items():
            # if value != self.plugin_manager.get_value(key):
            if self.plugin_manager.get_value(key, value) is False:
                # если плагин возвращает False то одно из правил в наборе правил не выполняется и редирект не выполняем
                return False

        return True 