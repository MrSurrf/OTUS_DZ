from flask import Blueprint, redirect, request
import logging
from container import AppContainer

logger = logging.getLogger(__name__)
bp = Blueprint('main', __name__)

# Получение экземпляра контейнера
container = AppContainer()

# Создание функции перенаправления
get_redirect_url = container.redirect_factory(
    container.rules_manager(),
    container.plugin_manager()
)

@bp.route('/')
def redirect_based_on_rules():
    """Основной маршрут для перенаправления на основе правил"""
    request_data = container.request_manager().extract_request_data(request)
    logger.info(f"Полученные данные запроса: {request_data}")
    logger.info(f"Правила: {container.rules_manager().get_rules()}")
    url = get_redirect_url(request_data)
    logger.info(f"Перенаправление на: {url}")
    return redirect(url)

