from aiogram.filters import BaseFilter
from aiogram.types import Message


class PasswordFilter(BaseFilter):
    def __init__(self, password: str):
        self.password = password

    async def __call__(self, message: Message) -> bool:
        return message.text == self.password
