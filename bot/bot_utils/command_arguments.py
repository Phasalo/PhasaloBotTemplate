from collections.abc import Callable

from aiogram.types import Message

from bot.bot_utils.di_utils import filter_kwargs
from db.repositories.users import UsersRepository
from phrases import PHRASES_RU


def multiple(_func: Callable | None = None, *, default=None):
    def decorator(func):
        async def wrapper(message: Message, **kwargs):
            parts = message.text.split()
            params = parts[1:]
            if not params:
                if default is not None:
                    return await func(message, [default], **kwargs)
                return await message.answer(PHRASES_RU.error.empty_argument)
            return await func(message, params, **kwargs)

        return wrapper

    return decorator(_func) if _func else decorator


def digit(_func: Callable | None = None, *, default=None):
    def decorator(func):
        @multiple(default=default)
        async def wrapper(message: Message, params, **kwargs):
            _digit = params[0]
            if not str(_digit).isdigit():
                return await message.answer(PHRASES_RU.error.not_digit_argument)
            return await func(message, int(_digit), **kwargs)

        return wrapper

    return decorator(_func) if _func else decorator


def user_id(func):
    @digit
    async def wrapper(message: Message, _user_id, **kwargs):
        users_repo: UsersRepository = await kwargs['dishka_container'].get(UsersRepository)
        if not users_repo.is_exists(_user_id):
            await message.answer(PHRASES_RU.replace('error.user_not_exist', user_id=_user_id))
            return
        kwargs['users_repo'] = users_repo
        await func(message, _user_id, **filter_kwargs(func, kwargs))

    return wrapper
