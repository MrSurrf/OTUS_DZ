# Создайте файл middleware.py
from flask import Flask, Request


class RequestMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Код, выполняемый до обработки запроса
        request = Request(environ)
        print(f"Processing request: {request.path} from {request.remote_addr}")

        # Можно изменить environ перед передачей запроса дальше

        # Перехватываем ответ для его модификации
        def custom_start_response(status, headers, exc_info=None):
            # Добавляем свой заголовок
            headers.append(('X-Powered-By', 'Redirect Rules Engine'))
            return start_response(status, headers, exc_info)

        # Передаем запрос дальше по цепочке middleware
        return self.app(environ, custom_start_response)


