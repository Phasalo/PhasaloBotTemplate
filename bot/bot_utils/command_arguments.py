from collections.abc import Callable

from aiogram.types import Message

from DB.tables.users import UsersTable
from phrases import PHRASES_RU


def multiple(_func: Callable | None = None, *, default=None):
    def decorator(func):
        async def wrapper(message: Message):
            parts = message.text.split()
            params = parts[1:]
            if not params:
                if default is not None:
                    return await func(message, [default])
                return await message.answer(PHRASES_RU.error.empty_argument)
            return await func(message, params)

        return wrapper

    return decorator(_func) if _func else decorator


def digit(_func: Callable | None = None, *, default=None):
    def decorator(func):
        @multiple(default=default)
        async def wrapper(message: Message, params):
            _digit = params[0]
            if not str(_digit).isdigit():
                return await message.answer(PHRASES_RU.error.not_digit_argument)
            return await func(message, int(_digit))

        return wrapper

    return decorator(_func) if _func else decorator


def user_id(func):
    @digit
    async def wrapper(message: Message, _user_id):
        with UsersTable() as users_db:
            if not users_db.is_exists(_user_id):
                await message.answer(PHRASES_RU.replace('error.user_not_exist', user_id=_user_id))
                return
            await func(message, _user_id)

    return wrapper
