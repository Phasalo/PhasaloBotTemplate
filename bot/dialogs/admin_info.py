from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Format

from config.const import QUERIES_PER_PAGE, USERS_PER_PAGE
from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable
from phrases import PHRASES_RU
from utils import format_list

from ._pagination import build_pagination_data, current_page, pagination_row, pagination_scroll


class UsersSG(StatesGroup):
    list = State()


class UserQuerySG(StatesGroup):
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


async def user_query_getter(dialog_manager: DialogManager, **kwargs):
    page = await current_page(dialog_manager)
    start_data: dict = dialog_manager.start_data  # type: ignore[assignment]
    user_id = int(start_data['user_id'])
    with QueriesTable() as queries_db, UsersTable() as users_db:
        queries, pagination = queries_db.get_user_queries(user_id, page, QUERIES_PER_PAGE)
        user = users_db.get_user(user_id)
    username_display = f'@{user.username}' if user and user.username else user.first_name if user else None
    return {
        'text': format_list.format_queries_text(
            queries=queries,
            name=username_display,
            user_id=user_id,
            footnote_template=PHRASES_RU.footnote.user_query,
            line_template=PHRASES_RU.template.user_query,
        ),
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

user_query_dialog = Dialog(
    Window(
        Format('{text}'),
        pagination_scroll(),
        pagination_row(),
        state=UserQuerySG.list,
        getter=user_query_getter,
        parse_mode='HTML',
    )
)
