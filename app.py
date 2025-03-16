import time
from flask import Flask, redirect, request, render_template_string, jsonify
from Container import Container
import os
import json
from RequestManager import RequestManager
from PluginManager import PluginManager
from middleware import RequestMiddleware

app = Flask(__name__)
app.wsgi_app = RequestMiddleware(app.wsgi_app)


@app.route('/')
def redirect_based_on_rules():
    running_request_manager = RequestManager()
    request_data = running_request_manager.extract_request_data(request)
    running_container = Container(request_data)
    while running_container.is_ready is not True:
        True
    url = running_container.get_redirect_url()
    print(url)
    return redirect(url)


@app.route('/editor')
def edit_rule():
    # Создаем экземпляр PluginManager с пустым словарем
    plugin_manager = PluginManager({})
    # Получаем словарь {ключ: имя} плагинов
    plugins_dict = plugin_manager.get_plugin_keys_and_names()

    html_template = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Редактор правил</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                padding: 20px;
                background-color: #f8f9fa;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
            }
            .card {
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .form-group {
                margin-bottom: 15px;
            }
            #rulesContainer {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                border: 1px solid #dee2e6;
                max-height: 400px;
                overflow-y: auto;
                font-family: monospace;
                white-space: pre-wrap;
            }
            .condition-row {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
                border: 1px solid #dee2e6;
            }
            .badge-plugin {
                margin-right: 5px;
                margin-bottom: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="my-4 text-center">Редактор правил перенаправления</h1>

            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Создание нового правила</h5>
                </div>
                <div class="card-body">
                    <form id="ruleForm">
                        <div class="form-group">
                            <label for="ruleName" class="form-label">Название правила:</label>
                            <input type="text" id="ruleName" name="ruleName" class="form-control" required>
                            <small class="form-text text-muted">Например: Правило для Windows и Chrome</small>
                        </div>

                        <div class="form-group">
                            <label for="redirectUrl" class="form-label">URL перенаправления:</label>
                            <input type="text" id="redirectUrl" name="redirectUrl" class="form-control" required>
                            <small class="form-text text-muted">Например: https://example.com</small>
                        </div>

                        <div class="form-group">
                            <label class="form-label">Условия правила:</label>
                            <div class="alert alert-info">
                                Добавьте одно или несколько условий для правила. Если условия не указаны, правило будет применяться ко всем запросам.
                            </div>

                            <div id="conditionsContainer">
                                <!-- Здесь будут добавляться строки с условиями -->
                            </div>

                            <div class="mt-2">
                                <button type="button" class="btn btn-outline-secondary" id="addConditionBtn">
                                    <i class="bi bi-plus-circle"></i> Добавить условие
                                </button>
                            </div>
                        </div>

                        <button type="button" id="submitRuleBtn" class="btn btn-primary">Сохранить правило</button>
                    </form>
                </div>
            </div>

            <div class="card">
                <div class="card-header bg-secondary text-white">
                    <h5 class="mb-0">Текущие правила</h5>
                </div>
                <div class="card-body">
                    <pre id="rulesContainer">Загрузка правил...</pre>
                    <button onclick="loadRules()" class="btn btn-outline-secondary mt-2">Обновить правила</button>
                </div>
            </div>
        </div>

        <!-- Шаблон для строки условия -->
        <template id="conditionRowTemplate">
            <div class="condition-row">
                <div class="row">
                    <div class="col-md-4">
                        <label class="form-label">Плагин:</label>
                        <select class="form-select plugin-select">
                            <option value="">Выберите плагин</option>
                            {% for key, name in plugins_dict.items() %}
                                <option value="{{ key }}">{{ name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="col-md-7">
                        <label class="form-label">Значение:</label>
                        <input type="text" class="form-control condition-value" placeholder="Введите значение">
                    </div>
                    <div class="col-md-1 d-flex align-items-end">
                        <button type="button" class="btn btn-outline-danger btn-sm remove-condition mb-2">
                            <span>&times;</span>
                        </button>
                    </div>
                </div>
            </div>
        </template>

        <script>
            // Отслеживание добавленных плагинов
            const addedPlugins = new Set();

            // Функция для проверки, добавлен ли уже плагин
            function isPluginAlreadyAdded(pluginKey) {
                return addedPlugins.has(pluginKey);
            }

            // Функция для обновления списка доступных плагинов
            function updateAvailablePlugins() {
                // Очищаем список добавленных плагинов
                addedPlugins.clear();

                // Заполняем список добавленных плагинов
                document.querySelectorAll('.plugin-select').forEach(select => {
                    const value = select.value;
                    if (value) {
                        addedPlugins.add(value);
                    }
                });

                // Обновляем все селекты, чтобы отключить уже выбранные плагины
                document.querySelectorAll('.plugin-select').forEach(select => {
                    const currentValue = select.value;

                    Array.from(select.options).forEach(option => {
                        const optionValue = option.value;
                        if (optionValue && optionValue !== currentValue && isPluginAlreadyAdded(optionValue)) {
                            option.disabled = true;
                        } else {
                            option.disabled = false;
                        }
                    });
                });
            }

            // Функция для добавления строки условия
            function addConditionRow() {
                const template = document.getElementById('conditionRowTemplate');
                const container = document.getElementById('conditionsContainer');

                const clone = document.importNode(template.content, true);
                container.appendChild(clone);

                // Добавляем обработчики событий
                const newRow = container.lastElementChild;
                const pluginSelect = newRow.querySelector('.plugin-select');
                const removeBtn = newRow.querySelector('.remove-condition');

                // Отключаем уже выбранные плагины в новом селекте
                Array.from(pluginSelect.options).forEach(option => {
                    const optionValue = option.value;
                    if (optionValue && isPluginAlreadyAdded(optionValue)) {
                        option.disabled = true;
                    }
                });

                pluginSelect.addEventListener('change', function() {
                    updateAvailablePlugins();
                });

                removeBtn.addEventListener('click', function() {
                    newRow.remove();
                    updateAvailablePlugins();
                });
            }

            // Функция для загрузки существующих правил
            function loadRules() {
                fetch('/get_rules')
                .then(response => response.json())
                .then(data => {
                    console.log("Текущие правила:", data);
                    document.getElementById('rulesContainer').innerText = JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    console.error('Ошибка загрузки правил:', error);
                    document.getElementById('rulesContainer').innerText = "Ошибка загрузки правил";
                });
            }

            // Функция для сбора данных формы
            function collectFormData() {
                const ruleName = document.getElementById('ruleName').value;
                const redirectUrl = document.getElementById('redirectUrl').value;

                // Проверяем обязательные поля
                if (!ruleName || !redirectUrl) {
                    alert('Пожалуйста, заполните название правила и URL перенаправления.');
                    return null;
                }

                // Собираем условия
                const params = {};
                const conditionRows = document.querySelectorAll('.condition-row');

                for (const row of conditionRows) {
                    const pluginKey = row.querySelector('.plugin-select').value;
                    const conditionValue = row.querySelector('.condition-value').value;

                    if (!pluginKey || !conditionValue) continue;

                    params[pluginKey] = conditionValue;
                }

                // Формируем данные правила
                return {
                    name: ruleName,
                    redirect: redirectUrl.startsWith('http') ? redirectUrl : 'https://' + redirectUrl,
                    params: params
                };
            }

            // Функция для отправки нового правила
            function submitRule() {
                const ruleData = collectFormData();
                if (!ruleData) return;

                fetch('/add_rule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(ruleData)
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);

                    // Очищаем форму
                    document.getElementById('ruleForm').reset();
                    document.getElementById('conditionsContainer').innerHTML = '';
                    addedPlugins.clear();

                    // Перезагружаем список правил
                    loadRules();
                })
                .catch(error => {
                    console.error('Ошибка при добавлении правила:', error);
                    alert('Ошибка при добавлении правила. Пожалуйста, попробуйте позже.');
                });
            }

            // Инициализация при загрузке страницы
            document.addEventListener('DOMContentLoaded', function() {
                // Загружаем существующие правила
                loadRules();

                // Добавляем обработчик для кнопки добавления условия
                document.getElementById('addConditionBtn').addEventListener('click', addConditionRow);

                // Добавляем обработчик для кнопки отправки формы
                document.getElementById('submitRuleBtn').addEventListener('click', submitRule);
            });
        </script>
    </body>
    </html>
    """

    return render_template_string(html_template, plugins_dict=plugins_dict)


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


if __name__ == '__main__':
    app.run(debug=True)