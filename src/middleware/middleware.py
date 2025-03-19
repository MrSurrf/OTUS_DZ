from flask import Flask, Request
import sys
import os
import logging

# Настраиваем логирование
logging.basicConfig(
    filename='middleware.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('middleware')


class RequestMiddleware:
    def __init__(self, app):
        self.app = app
        logger.info("=== MIDDLEWARE INITIALIZED ===")
        print("=== MIDDLEWARE INITIALIZED ===", file=sys.stderr)       
        logger.info(f"Содержимое текущей директории: {os.listdir('.')}")

    def __call__(self, environ, start_response):        
        request = Request(environ)
        logger.info("="*50)
        logger.info(f"Processing request: {request.path} from {request.remote_addr}")
        
        
        print("="*50)
        print(f"MIDDLEWARE: Processing request: {request.path} from {request.remote_addr}")
        
        # Перехватываем ответ для его модификации
        def custom_start_response(status, headers, exc_info=None):
            # Добавляем свой заголовок
            headers.append(('Created-By', 'SRV_developer'))
            logger.info(f"Response status: {status}")
            print(f"MIDDLEWARE: Response status: {status}", file=sys.stderr)
            return start_response(status, headers, exc_info)

        # Передаем запрос дальше по цепочке middleware
        return self.app(environ, custom_start_response)


