from .plugins_interfaces import PluginInterface
import logging

logger = logging.getLogger(__name__)

class Plugin_OS(PluginInterface):
    def get_name(self):
        return "os"

    def run(self, rules, request_data):
        user_agent = request_data['headers'].get('User-Agent', '').lower()
        logger.info(f"User-Agent: {user_agent}")

        if rules[0] == "os":
            # os_rules = rules.get('os', {})
            for os, url in rules[1].items():
                if os.lower() in user_agent:
                    return url
        return None

