from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Format

from config.const import QUERIES_PER_PAGE, USERS_PER_PAGE
from db.repositories.queries import QueriesRepository
from db.repositories.users import UsersRepository
from phrases import PHRASES_RU
from utils import format_list

from ._pagination import build_pagination_data, current_page, pagination_row, pagination_scroll


class UsersSG(StatesGroup):
    list = State()


class UserQuerySG(StatesGroup):
    list = State()


async def users_getter(dialog_manager: DialogManager, **kwargs):
    container = kwargs['dishka_container']
    users_repo: UsersRepository = await container.get(UsersRepository)
    page = await current_page(dialog_manager)
    users, pagination = users_repo.get_all_users(page, USERS_PER_PAGE)
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
    container = kwargs['dishka_container']
    users_repo: UsersRepository = await container.get(UsersRepository)
    queries_repo: QueriesRepository = await container.get(QueriesRepository)
    page = await current_page(dialog_manager)
    start_data: dict = dialog_manager.start_data  # type: ignore[assignment]
    user_id = int(start_data['user_id'])
    queries, pagination = queries_repo.get_user_queries(user_id, page, QUERIES_PER_PAGE)
    user = users_repo.get_user(user_id)
    username_display = user.display_name() if user else None
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
