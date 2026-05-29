import typing

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.bot_utils.di_utils import filter_kwargs
from bot.bot_utils.filters import AdminFilter
from bot.bot_utils.models import CommandUnit


class BaseRouter(Router):
    available_commands: typing.ClassVar[list[CommandUnit]] = []
    is_admin: bool = False  # По умолчанию не админский роутер

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_admin:
            self.message.filter(AdminFilter())

    def command(self, command: str | tuple[str, ...], description: str = '', *placeholders):
        def decorator(handler):
            commands = (command,) if isinstance(command, str) else command
            self.available_commands.append(
                CommandUnit(
                    commands[0], commands[1:], description, self.is_admin, placeholders if placeholders else None
                )
            )

            @self.message(Command(*commands, ignore_case=True))
            async def wrapper(message: Message, **kwargs):
                await handler(message, **filter_kwargs(handler, kwargs))

            return handler

        return decorator


class AdminRouter(BaseRouter):
    is_admin = True


class UserRouter(BaseRouter):
    is_admin = False
