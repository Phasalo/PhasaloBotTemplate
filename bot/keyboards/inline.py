from aiogram.types import InlineKeyboardButton as IButton
from aiogram.types import InlineKeyboardMarkup as IMarkup

from bot.bot_utils.models import PageCallBack
from DB.models import Pagination
from phrases import PHRASES_RU


def page_keyboard(type_of_event: int, pagination: Pagination, user_id: int = 0) -> IMarkup | None:
    if pagination.total_pages <= 1:
        return None

    empty_button = IButton(text=' ', callback_data=PageCallBack(type_of_event=-1).pack())

    past_button = (
        IButton(
            text=PHRASES_RU.button.past_page,
            callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page - 1, user_id=user_id).pack(),
        )
        if pagination.has_prev
        else empty_button
    )

    next_button = (
        IButton(
            text=PHRASES_RU.button.next_page,
            callback_data=PageCallBack(type_of_event=type_of_event, page=pagination.page + 1, user_id=user_id).pack(),
        )
        if pagination.has_next
        else empty_button
    )

    return IMarkup(
        inline_keyboard=[
            [
                past_button,
                IButton(
                    text=PHRASES_RU.replace(
                        'template.page_counter', current=pagination.page, total=pagination.total_pages
                    ),
                    callback_data=PageCallBack(
                        type_of_event=type_of_event, page=pagination.page, user_id=user_id
                    ).pack(),
                ),
                next_button,
            ]
        ]
    )
