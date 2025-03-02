from flask import Flask, redirect, request, render_template_string, jsonify
from container import AppContainer
from Plugin_manager import PluginManager
import logging
import os
import json

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
container = AppContainer()
plugins = PluginManager("handlers")


# Конфигурация контейнера
container.config.from_dict({
    'rules_file': 'rule.json',
    'handlers_dir': 'handlers'
})

# Создание функции перенаправления
get_redirect_url = container.redirect_factory(
    container.rules_manager(),
    container.plugin_manager()
)

# Глобальная переменная для хранения списка плагинов (загружаем один раз)
LOADED_PLUGINS = None

def load_plugins_once():
    global LOADED_PLUGINS
    if LOADED_PLUGINS is None:
        plugins.load_plugins()
        LOADED_PLUGINS = plugins.get_plugin_names()

@app.route('/')
def redirect_based_on_rules():

    request_data = container.request_manager().extract_request_data(request)
    logger.info(f"Полученные данные запроса: {request_data}")
    logger.info(f"Правила: {container.rules_manager().get_rules()}")
    url = get_redirect_url(request_data)
    return redirect(url)


@app.route('/editor')
def edit_rule():
    # plugins.load_plugins()
    # plugins_name = plugins.get_plugin_names()  # Получаем список имен плагинов
    load_plugins_once()

    html_template = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Редактор правил</title>
    </head>
    <body>
        <h2>Выберите плагин:</h2>
        <form id="ruleForm">
            <label for="plugin">Плагин:</label>
            <select name="plugin" id="plugin">
                {% for name in plugins_name %}
                    <option value="{{ name }}">{{ name }}</option>
                {% endfor %}
            </select>
            <br>
            <label for="param1">Параметр 1:</label>
            <input type="text" id="param1" name="param1" required>
            <br>
            <label for="param2">Параметр 2 (ссылка):</label>
            <input type="text" id="param2" name="param2" required>
            <br>
            <button type="button" onclick="submitRule()">Применить</button>
        </form>
        <script>
            function loadRules() {
                fetch('/get_rules')
                .then(response => response.json())
                .then(data => {
                    console.log("Текущие правила:", data);
                    document.getElementById('rulesContainer').innerText = JSON.stringify(data, null, 2);
                })
                .catch(error => console.error('Ошибка загрузки правил:', error));
            }
        
            document.addEventListener("DOMContentLoaded", loadRules);
        </script>
        <pre id="rulesContainer"></pre>

        <script>
            function submitRule() {
                const formData = new FormData(document.getElementById('ruleForm'));
                fetch('/apply_rule', {
                    method: 'POST',
                    body: JSON.stringify(Object.fromEntries(formData)),
                    headers: { 'Content-Type': 'application/json' }
                })
                .then(response => response.json())
                .then(data => alert(data.message))
                .catch(error => console.error('Ошибка:', error));
            }
        </script>
    </body>
    </html>
    """

    return render_template_string(html_template, plugins_name=LOADED_PLUGINS)


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



if __name__ == '__main__':
    container.plugin_manager().load_plugins()
    logger.info(f"Загруженные плагины: {[plugin.get_name() for plugin in container.plugin_manager().get_plugins()]}")
    app.run(debug=True)

