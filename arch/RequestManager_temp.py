class RequestManager:
    def extract_request_data(self, request):
        return {
            'browser': 'Chrome',
            'browser_version': '120.0',
            'os': 'Windows',
            'os_version': '10',
            'device': 'PC',
            'is_mobile': False,
            'is_tablet': False,
            'is_pc': True,
            'is_bot': False,
            'user_agent': request.headers.get('User-Agent'),
            'ip': request.remote_addr,
            'path': request.path,
            'args': dict(request.args),
            'headers': dict(request.headers),
            'method': request.method,
            'cookies': dict(request.cookies),
            'time': '12:00'
        } 