import datetime

from user_agents import parse

class RequestManager:
    def extract_request_data(self, request):
        user_agent_string = request.headers.get('User-Agent')

        user_agent = parse(user_agent_string)


        return {
            'browser': user_agent.browser.family,
            'browser_version': user_agent.browser.version_string,
            'os': user_agent.os.family,
            'os_version': user_agent.os.version_string,
            'device': user_agent.device.family,
            'is_mobile': user_agent.is_mobile,
            "is_tablet": user_agent.is_tablet,
            "is_pc": user_agent.is_pc,
            "is_bot": user_agent.is_bot,

            'user_agent': request.headers.get('User-Agent'),
            'ip': request.remote_addr,
            'path': request.path,
            'args': dict(request.args),
            'headers': dict(request.headers),
            'method': request.method,
            'cookies': dict(request.cookies)
        }

