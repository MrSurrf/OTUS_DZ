from flask import redirect, request, render_template_string, jsonify
import os
import json
from Container import Container
from templates import EDITOR_TEMPLATE


def init_routes(app):
    @app.route('/')
    def redirect_based_on_rules():
        request_manager = app.container.request_manager()
        request_data = request_manager.extract_request_data(request)
        running_container = Container(request_data)
        while running_container.is_ready is not True:
            True
        url = running_container.get_redirect_url()
        print(url)
        return redirect(url)

    @app.route('/editor')
    def edit_rule():
        # Получаем PluginManager через DI контейнер
        plugin_manager = app.container.plugin_manager()
        # Получаем словарь {ключ: имя} плагинов
        plugins_dict = plugin_manager.get_plugin_keys_and_names()
        return render_template_string(EDITOR_TEMPLATE, plugins_dict=plugins_dict)

    @app.route('/add_rule', methods=['POST'])
    def add_rule():
        data = request.json
        name = data.get("name")
        redirect_url = data.get("redirect")
        params = data.get("params", {})

        if not name or not redirect_url:
            return jsonify({"message": "Ошибка: название и URL перенаправления обязательны!"}), 400

        # Загружаем текущие правила
        if os.path.exists('rule.json'):
            with open('rule.json', "r", encoding="utf-8") as file:
                try:
                    rules = json.load(file)
                    if not isinstance(rules, list):
                        rules = []
                except json.JSONDecodeError:
                    rules = []
        else:
            rules = []

        # Создаем новое правило
        new_rule = {
            "name": name,
            "redirect": redirect_url,
            "params": params
        }

        # Добавляем правило в список
        rules.append(new_rule)

        # Сохраняем обновленный список правил
        with open('rule.json', "w", encoding="utf-8") as file:
            json.dump(rules, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Правило успешно добавлено!"})

    @app.route('/apply_rule', methods=['POST'])
    def apply_rule():
        data = request.json
        plugin_name = data.get("plugin")
        param1 = data.get("param1")
        param2 = data.get("param2")

        if not plugin_name or not param1 or not param2:
            return jsonify({"message": "Ошибка: все поля должны быть заполнены!"}), 400

        # Загружаем текущие правила
        if os.path.exists('rule.json'):
            with open('rule.json', "r", encoding="utf-8") as file:
                rules = json.load(file)
        else:
            rules = {}

        # Добавляем или обновляем правило
        if plugin_name not in rules:
            rules[plugin_name] = {param1: param2}  # Создаем новый блок правил
        else:
            rules[plugin_name][param1] = param2  # Добавляем новое условие

        # Сохраняем изменения в JSON
        with open('rule.json', "w", encoding="utf-8") as file:
            json.dump(rules, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Правило успешно обновлено!"})

    @app.route('/get_rules', methods=['GET'])
    def get_rules():
        if os.path.exists('rule.json'):
            with open('rule.json', "r", encoding="utf-8") as file:
                rules = json.load(file)
        else:
            rules = {}

        return jsonify(rules) 