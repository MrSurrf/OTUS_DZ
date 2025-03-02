from flask import Blueprint, render_template, request
import logging
from Plugin_manager import PluginManager

logger = logging.getLogger(__name__)
bp = Blueprint('editor', __name__)

# Инициализация менеджера плагинов
plugins = PluginManager("handlers")

# Глобальная переменная для хранения списка плагинов (загружаем один раз)
LOADED_PLUGINS = None

def load_plugins_once():
    """Загружает плагины один раз и сохраняет их имена"""
    global LOADED_PLUGINS
    if LOADED_PLUGINS is None:
        plugins.load_plugins()
        LOADED_PLUGINS = plugins.get_plugin_names()
    return LOADED_PLUGINS

@bp.route('/editor')
def edit_rule():
    """Страница редактора правил"""
    plugins_name = load_plugins_once()
    return render_template('editor.html', plugins_name=plugins_name)
