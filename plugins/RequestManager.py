class RequestManager:
    def extract_request_data(self, request):
        return {
            'user_agent': request.headers.get('User-Agent'),
            'ip': request.remote_addr,
            'path': request.path,
            'args': dict(request.args),
            'headers': dict(request.headers),
            'method': request.method,
            'cookies': dict(request.cookies)
        }

