from flask import Flask, request, g
from src.di.containers import DIContainer
from src.routes.routes import init_routes
import sys
import time

print("Importing middleware...", file=sys.stderr)
from src.middleware.middleware import RequestMiddleware
print("Middleware imported successfully!", file=sys.stderr)


def create_app():
    app = Flask(__name__)
    app.container = DIContainer()    
    # Подключаем middleware
    print("Connecting middleware to app...", file=sys.stderr)
    app.wsgi_app = RequestMiddleware(app.wsgi_app)
    print("Middleware connected!", file=sys.stderr)

    init_routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 