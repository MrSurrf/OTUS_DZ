from .plugins_interfaces import PluginInterface

class Plugin_User_Agent(PluginInterface):
    def get_name(self):
        return "browser"

    def run(self, rules, request_data):
        user_agent = request_data['headers'].get('User-Agent', '').lower()
        # browser_rules = rules.get('browser', {})
        if rules[0] == 'browser':
            for browser, url in rules[1].items():
                if browser.lower() in user_agent:
                    return url
        return None

