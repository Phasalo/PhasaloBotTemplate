import inspect
from collections.abc import Callable

from aiogram.types import Message

from db.repositories.users import UsersRepository
from phrases import PHRASES_RU


async def _resolve(func, kwargs: dict) -> dict:
    sig = inspect.signature(func)
    has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
    resolved = dict(kwargs) if has_var_keyword else {k: v for k, v in kwargs.items() if k in sig.parameters}
    container = kwargs.get('dishka_container')
    if container:
        for name, param in sig.parameters.items():
            if name not in resolved and param.annotation is not inspect.Parameter.empty:
                try:
                    resolved[name] = await container.get(param.annotation)
                except Exception:
                    pass
    return resolved


def multiple(_func: Callable | None = None, *, default=None):
    def decorator(func):
        async def wrapper(message: Message, **kwargs):
            parts = message.text.split()
            params = parts[1:]
            resolved = await _resolve(func, kwargs)
            if not params:
                if default is not None:
                    return await func(message, [default], **resolved)
                return await message.answer(PHRASES_RU.error.empty_argument)
            return await func(message, params, **resolved)

        return wrapper

    return decorator(_func) if _func else decorator


def digit(_func: Callable | None = None, *, default=None):
    def decorator(func):
        @multiple(default=default)
        async def wrapper(message: Message, params, **kwargs):
            _digit = params[0]
            if not str(_digit).isdigit():
                return await message.answer(PHRASES_RU.error.not_digit_argument)
            return await func(message, int(_digit), **await _resolve(func, kwargs))

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
        await func(message, _user_id, **await _resolve(func, kwargs))

    return wrapper
