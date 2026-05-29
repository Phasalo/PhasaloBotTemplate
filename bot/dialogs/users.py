from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Format

from config.const import USERS_PER_PAGE
from DB.tables.users import UsersTable
from utils import format_list

from ._pagination import build_pagination_data, current_page, pagination_row, pagination_scroll


class UsersSG(StatesGroup):
    list = State()


async def users_getter(dialog_manager: DialogManager, **kwargs):
    page = await current_page(dialog_manager)
    with UsersTable() as db:
        users, pagination = db.get_all_users(page, USERS_PER_PAGE)
    return {
        'text': format_list.format_user_list(users, pagination),
        **build_pagination_data(
            dialog_manager,
            pagination.total_pages,
            pagination.has_prev,
            pagination.has_next,
        ),
    }


users_dialog = Dialog(
    Window(
        Format('{text}'),
        pagination_scroll(),
        pagination_row(),
        state=UsersSG.list,
        getter=users_getter,
        parse_mode='HTML',
    )
)
