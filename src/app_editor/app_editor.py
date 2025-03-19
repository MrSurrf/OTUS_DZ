from flask import redirect, request, render_template_string, jsonify, Flask
import os
import json
import sys
from src.di.Container import Container
from src.app_editor.templates import EDITOR_TEMPLATE
from src.di.containers import DIContainer

def editor_app():
    # Получаем путь к корневой директории проекта
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rules_file = os.path.join(base_dir, 'rule.json')
    print(f"Путь к файлу правил: {rules_file}")

    app = Flask(__name__)
    app.container = DIContainer()

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
        if os.path.exists(rules_file):
            with open(rules_file, "r", encoding="utf-8") as file:
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
        with open(rules_file, "w", encoding="utf-8") as file:
            json.dump(rules, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Правило успешно добавлено!"})
    
    @app.route('/get_rules', methods=['GET'])
    def get_rules():
        if os.path.exists(rules_file):
            with open(rules_file, "r", encoding="utf-8") as file:
                try:
                    rules = json.load(file)
                    print(f"Загружены правила: {rules}")
                except json.JSONDecodeError as e:
                    print(f"Ошибка при чтении JSON: {e}")
                    rules = []
        else:
            print(f"Файл правил не найден по пути: {rules_file}")
            rules = []

        return jsonify(rules)

    @app.route('/delete_rule', methods=['POST'])
    def delete_rule():
        data = request.json
        rule_name = data.get("name")

        if not rule_name:
            return jsonify({"message": "Ошибка: название правила обязательно!"}), 400

        # Загружаем текущие правила
        if os.path.exists(rules_file):
            with open(rules_file, "r", encoding="utf-8") as file:
                try:
                    rules = json.load(file)
                    if not isinstance(rules, list):
                        return jsonify({"message": "Ошибка: некорректный формат правил!"}), 500
                except json.JSONDecodeError:
                    return jsonify({"message": "Ошибка: некорректный JSON!"}), 500
        else:
            return jsonify({"message": "Ошибка: файл правил не найден!"}), 404

        # Ищем и удаляем правило с указанным именем
        found = False
        rules_new = []
        for rule in rules:
            if rule.get("name") != rule_name:
                rules_new.append(rule)
            else:
                found = True

        if not found:
            return jsonify({"message": f"Ошибка: правило с именем '{rule_name}' не найдено!"}), 404

        # Сохраняем обновленный список правил
        with open(rules_file, "w", encoding="utf-8") as file:
            json.dump(rules_new, file, ensure_ascii=False, indent=4)

        return jsonify({"message": f"Правило '{rule_name}' успешно удалено!"}) 

    return app

if __name__ == '__main__':
    app = editor_app()
    app.run(port=5001)