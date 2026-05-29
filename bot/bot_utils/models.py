from dataclasses import dataclass
from typing import Any


@dataclass
class CommandUnit:
    """Контейнер для хранения информации о команде бота"""

    name: str  # Основное имя команды
    aliases: tuple[str, ...] = ()  # Дополнительные варианты вызова
    description: str = ''
    is_admin: bool = False
    placeholders: tuple[Any, ...] | None = None

    def __str__(self):
        base = f'/{self.name}'
        if self.aliases:
            base += f', {", ".join(f"/{a}" for a in self.aliases)}'
        if self.placeholders:
            base += ' ' + ' '.join(f'{{{p}}}' for p in self.placeholders)
        if self.description:
            base += f' — {self.description}'
        return base
