from flask import Flask
from containers import DIContainer
from routes import init_routes


def create_app():
    app = Flask(__name__)
    app.container = DIContainer()
    init_routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)