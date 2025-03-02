import json
import logging

logger = logging.getLogger(__name__)


class RulesManager:
    def __init__(self, rules_file):
        self.rules_file = rules_file
        self._load_rules()

    def _load_rules(self):
        """Загружает правила из JSON-файла"""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
            logger.info(f"Правила успешно загружены из {self.rules_file}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке правил: {e}")
            self.rules = {}

    def get_rules(self):
        """Возвращает загруженные правила"""
        return self.rules

