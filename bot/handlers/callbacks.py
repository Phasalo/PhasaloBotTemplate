from aiogram import Router
from aiogram.types import CallbackQuery

from bot import pages
from bot.bot_utils.models import PageCallBack

router = Router()


@router.callback_query(PageCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PageCallBack):
    type_of_event = callback_data.type_of_event
    page = callback_data.page
    user_id = callback_data.user_id
    await callback.answer()
    if type_of_event == 1:
        await pages.get_users(callback.from_user.id, page, callback.message.message_id)
    elif type_of_event == 2:
        await pages.user_query(callback.from_user.id, user_id, page, callback.message.message_id)
    elif type_of_event == -1:
        pass
