import os
import json
import logging
import RuleBuilder
logger = logging.getLogger(__name__)


class RulesManager:
    def __init__(self, rules_file):
        self.rules_file = rules_file
        self.rules = []
        self._load_rules()

    def _load_rules(self):
        """Загружает правила из JSON-файла"""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                self.rules_data = json.load(f)
                print(self.rules_data)
            logger.info(f"Успешно загружено {len(self.rules_data)} правил из {self.rules_file}")

        except FileNotFoundError:
            logger.error(f"Файл {self.rules_file} не найден")
            self.rules_data = []
        except json.JSONDecodeError:
            logger.error(f"Ошибка формата JSON в файле {self.rules_file}")
            self.rules_data = []
        except Exception as e:
            logger.error(f"Ошибка при загрузке правил: {e}")
            self.rules_data = []

    def get_rules(self):
        """Возвращает загруженные правила"""
        return self.rules_data

