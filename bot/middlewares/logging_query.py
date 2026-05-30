import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import InlineQuery, Message, TelegramObject

from bot.bot_utils.routers import BaseRouter
from db.models import QueryModel, UserModel
from db.repositories.queries import QueriesRepository

logger = logging.getLogger(__name__)


class UserLoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        #   <-| ----------------- -<phasalo>- ------------------ |->
        #                                                          |
        #     логгирование или своя логика                         | <=| PHASALO<|||
        #                                                          |
        #   <-| ----------------- -<phasalo>- ------------------ |->

        # phasalo ON
        if isinstance(event, Message):
            skip_commands = [
                f'/{cmd}'
                for command in BaseRouter.available_commands
                if command.is_admin
                for cmd in [command.name, *list(command.aliases)]
            ]
            if event.text and any(event.text.startswith(cmd) for cmd in skip_commands):
                return await handler(event, data)
        user_row: UserModel | None = data.get('user_row')
        if user_row is None:
            logger.warning("Cannot add queries. The 'user_row' key was not found in the middleware data.")
            return await handler(event, data)

        queries_repo: QueriesRepository = await data['dishka_container'].get(QueriesRepository)

        # Логируем текстовые сообщения
        if isinstance(event, Message) and event.text:
            queries_repo.add_query(QueryModel(user_row.user_id, event.text))

        # Логируем инлайн-запросы
        elif isinstance(event, InlineQuery) and event.query:
            queries_repo.add_query(QueryModel(user_row.user_id, f'[INLINE] {event.query}'))
        # phasalo OFF

        return await handler(event, data)
