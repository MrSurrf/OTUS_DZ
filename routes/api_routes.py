from flask import Blueprint, request, jsonify
import logging
import os
import json

logger = logging.getLogger(__name__)
bp = Blueprint('api', __name__)

@bp.route('/apply_rule', methods=['POST'])
def apply_rule():
    """API-маршрут для применения правила"""
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

@bp.route('/get_rules', methods=['GET'])
def get_rules():
    """API-маршрут для получения правил"""
    if os.path.exists('rule.json'):
        with open('rule.json', "r", encoding="utf-8") as file:
            rules = json.load(file)
    else:
        rules = {}

    return jsonify(rules)

