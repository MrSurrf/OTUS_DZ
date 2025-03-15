import time
from flask import Flask, redirect, request, render_template_string, jsonify
# from container import AppContainer
# from Plugin_manager import PluginManager
from Container import Container
# import logging
import os
import json
from RequestManager import RequestManager


app = Flask(__name__)

@app.route('/')
def redirect_based_on_rules():
    running_request_manager = RequestManager()
    # request_data = container.request_manager().extract_request_data(request)
    request_data = running_request_manager.extract_request_data(request)
    running_container = Container(request_data)
    # logger.info(f"Полученные данные запроса: {request_data}")
    # logger.info(f"Правила: {container.rules_manager().get_rules()}")
    while running_container.is_ready is not True:
        True
    url = running_container.get_redirect_url()
    print(url)
    return redirect(url)


@app.route('/editor')
def edit_rule():
    html_template = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Редактор правил</title>
    </head>
    <body>
        <h2>Создание правила перенаправления</h2>
        <form id="ruleForm">
            <label>Операционная система:</label>
            <input type="text" id="os" name="os">
            <br>
            <label>Браузер:</label>
            <input type="text" id="browser" name="browser">
            <br>
            <label>Временной диапазон (часы, через дефис):</label>
            <input type="text" id="time" name="time" placeholder="09-18">
            <br>
            <label>URL перенаправления:</label>
            <input type="text" id="redirect_url" name="redirect_url" required>
            <br>
            <button type="button" onclick="submitRule()">Добавить правило</button>
        </form>
        <pre id="rulesContainer"></pre>
        <script>
            function loadRules() {
                fetch('/get_rules')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('rulesContainer').innerText = JSON.stringify(data, null, 2);
                })
                .catch(error => console.error('Ошибка загрузки правил:', error));
            }

            function submitRule() {
                const os = document.getElementById("os").value || null;
                const browser = document.getElementById("browser").value || null;
                const time = document.getElementById("time").value || null;
                const redirect_url = document.getElementById("redirect_url").value;

                if (!redirect_url) {
                    alert("URL перенаправления обязателен!");
                    return;
                }

                const ruleData = { os, browser, time, redirect_url };

                fetch('/apply_rule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(ruleData)
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    loadRules();
                })
                .catch(error => console.error('Ошибка:', error));
            }

            document.addEventListener("DOMContentLoaded", loadRules);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)


@app.route('/apply_rule', methods=['POST'])
def apply_rule():
    data = request.json
    redirect_url = data.get("redirect_url")

    if not redirect_url:
        return jsonify({"message": "Ошибка: URL должен быть заполнен!"}), 400

    if not redirect_url.startswith(("http://", "https://")):
        redirect_url = "https://" + redirect_url

    rule_entry = {"redirect": redirect_url}

    # Добавляем в rule_entry только непустые параметры
    optional_fields = ["os", "browser", "time"]
    for field in optional_fields:
        value = data.get(field)
        if value:  # Записываем только непустые значения
            rule_entry[field] = value

    if os.path.exists('rule.json'):
        with open("rule.json", "r", encoding="utf-8") as file:
            try:
                rules = json.load(file)
                if not isinstance(rules, list):  # Исправляем структуру, если в файле не список
                    rules = []
            except json.JSONDecodeError:
                rules = []  # Если JSON повреждён
    else:
        rules = []

    rules.append(rule_entry)

    with open("rule.json", "w", encoding="utf-8") as file:
        json.dump(rules, file, ensure_ascii=False, indent=4)

    return jsonify({"message": "Правило успешно добавлено!"})


@app.route('/get_rules', methods=['GET'])
def get_rules():
    if os.path.exists('rule.json'):
        with open('rule.json', "r", encoding="utf-8") as file:
            rules = json.load(file)
    else:
        rules = {}

    return jsonify(rules)


if __name__ == '__main__':
    # container.plugin_manager().load_plugins()
    # logger.info(f"Загруженные плагины: {[plugin.get_name() for plugin in container.plugin_manager().get_plugins()]}")
    app.run(debug=True, use_reloader=False)
