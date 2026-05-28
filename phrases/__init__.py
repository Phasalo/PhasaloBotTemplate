import re
from os.path import dirname
from random import choice
from typing import Any

import yaml


class Phrases:
    def __init__(self, dictionary: dict[str, Any]):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, Phrases(value))
            else:
                setattr(self, key, value)

    def __getattribute__(self, name: str):
        value = object.__getattribute__(self, name)

        if isinstance(value, list):
            return choice(value)
        return value

    def __getattr__(self, name: str):
        raise AttributeError(f'Фраза «{name}» не найдена')

    def __repr__(self):
        return str(self.__dict__)

    def replace(self, phrase_name: str, **replacements: Any) -> str:
        """
        Получает фразу с заменой плейсхолдеров

        :param phrase_name: Название фразы (например 'success.user_banned')
        :param replacements: Параметры для замены (например user_id=123)
        :return: Готовая фраза с подставленными значениями
        """
        parts = phrase_name.split('.')
        current = self

        try:
            for part in parts:
                current = getattr(current, part)
        except AttributeError as err:
            raise AttributeError(f'Фраза «{phrase_name}» не найдена') from err

        if isinstance(current, list):
            phrase = choice(current)
        else:
            phrase = current

        # Заменяем все плейсхолдеры вида {key}
        for key, value in replacements.items():
            pattern = re.compile(r'\{\s*' + re.escape(key) + r'\s*}')
            phrase = pattern.sub(str(value), phrase)

        return phrase


def __load_phrases(phrases_path: str) -> Phrases:
    with open(phrases_path, encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return Phrases(data)


PHRASES_RU = __load_phrases(f'{dirname(__file__)}/phrases_ru.yaml')
