from flask import Blueprint

# Импортируем все маршруты
from .main_routes import bp as main_bp
from .editor_routes import bp as editor_bp
from .api_routes import bp as api_bp

# Создаем основной Blueprint для всех маршрутов
routes = Blueprint('routes', __name__)

# Регистрируем все Blueprint'ы
routes.register_blueprint(main_bp)
routes.register_blueprint(editor_bp)
routes.register_blueprint(api_bp)

# Функция для инициализации всех маршрутов
def init_app(app):
    app.register_blueprint(routes)
