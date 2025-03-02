from .plugins_interfaces import PluginInterface
from datetime import datetime

class Plugin_Time_Based(PluginInterface):
    def get_name(self):
        return "time"

    def run(self, rules, request_data):
        now = datetime.now().strftime("%H:%M")
        # time_rules = rules.get('time', {})
        if rules[0] == "time":
            for time_range, url in rules[1].items():
                start, end = time_range.split('-')
                if start <= now <= end:
                    return url
        return None

