import time

from IPlugins import IPlugins
import datetime

class PluginOS(IPlugins):

    def __init__(self):
        self.needs_data = True
        self.name = "Время"
        self.keys = 'time'
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
        print(rule_value)
        # Получаем текущее серверное время (или время из запроса)
        current_time = datetime.datetime.now().time()
        print(f"Текущее время сервера: {current_time}")
        a = "12:00 - 16:00"

        start_str, end_str = rule_value.split("-")
        start_time = datetime.datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.datetime.strptime(end_str, "%H:%M").time()

        print(f"Проверяем, попадает ли {current_time} в диапазон {start_time} - {end_time}")
        # Проверяем попадание в диапазон
        if start_time <= end_time:
            return start_time <= current_time <= end_time
        else:
            # Обрабатываем случай, когда диапазон пересекает полночь (например, "23:00 - 02:00")
            return current_time >= start_time or current_time <= end_time
