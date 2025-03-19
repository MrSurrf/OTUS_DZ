from flask import redirect, request, render_template_string, jsonify
import os
import json
from src.di.Container import Container
from src.app_editor.templates import EDITOR_TEMPLATE


def init_routes(app):
    @app.route('/')
    def redirect_based_on_rules():    
        request_manager = app.container.request_manager()
        request_data = request_manager.extract_request_data(request)
        running_container = Container(request_data, app)
        
        url = running_container.get_redirect_url()
        print(url)
        return redirect(url)

    # @app.route('/editor')
    # def edit_rule():
    #     # Получаем PluginManager через DI контейнер
    #     plugin_manager = app.container.plugin_manager()
    #     # Получаем словарь {ключ: имя} плагинов
    #     plugins_dict = plugin_manager.get_plugin_keys_and_names()
    #     return render_template_string(EDITOR_TEMPLATE, plugins_dict=plugins_dict)
