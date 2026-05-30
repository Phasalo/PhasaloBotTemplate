import logging

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

import temp
from bot.bot_utils import command_arguments
from bot.bot_utils.routers import AdminRouter, BaseRouter
from bot.dialogs import UserQuerySG, UsersSG
from config.const import QUERIES_PER_PAGE
from db.repositories.queries import QueriesRepository
from db.repositories.users import UsersRepository
from phrases import PHRASES_RU
from utils import format_list

router = AdminRouter()
logger = logging.getLogger(__name__)


@router.command(('users', 'u'), 'таблица со всеми пользователями')  # /users
async def _(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UsersSG.list, mode=StartMode.RESET_STACK)


@router.command(('commands', 'cmds'), 'список всех доступных команд')  # /commands /cmds
async def command_getcmds(message: Message):
    commands_text = PHRASES_RU.title.commands
    admin_commands = '\n'.join(str(command) for command in BaseRouter.available_commands if command.is_admin)
    if admin_commands:
        commands_text += PHRASES_RU.subtitle.admin_commands + admin_commands
    user_commands = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    if user_commands:
        commands_text += PHRASES_RU.subtitle.user_commands + user_commands
    await message.answer(commands_text)


@router.command('ban', 'заблокировать пользователя по ID', 'user_id')  # /ban
@command_arguments.user_id
async def _(message: Message, user_id, users_repo: UsersRepository):
    if message.from_user.id == int(user_id):
        await message.answer(PHRASES_RU.error.ban_yourself)
        return
    if users_repo.set_ban_status(user_id, message.from_user.id, True):
        await message.answer(PHRASES_RU.replace('success.banned', user_id=user_id))
    else:
        await message.answer(PHRASES_RU.error.db)


@router.command('unban', 'разблокировать пользователя по ID', 'user_id')  # /unban
@command_arguments.user_id
async def _(message: Message, user_id, users_repo: UsersRepository):
    if users_repo.set_ban_status(user_id, message.from_user.id, False):
        await message.answer(PHRASES_RU.replace('success.unbanned', user_id=user_id))
    else:
        await message.answer(PHRASES_RU.error.db)


@router.command('promote', 'повысить уровень доступа', 'user_id')  # /promote
@command_arguments.user_id
async def _(message: Message, user_id, users_repo: UsersRepository):
    if users_repo.set_admin(user_id, message.from_user.id, True):
        await message.answer(PHRASES_RU.replace('success.promoted_by', user_id=user_id))
    else:
        await message.answer(PHRASES_RU.error.db)


@router.command('demote', 'понизить уровень доступа', 'user_id')  # /demote
@command_arguments.user_id
async def _(message: Message, user_id, users_repo: UsersRepository):
    if users_repo.set_admin(user_id, message.from_user.id, False):
        await message.answer(PHRASES_RU.replace('success.demoted', user_id=user_id))
    else:
        await message.answer(PHRASES_RU.error.db)


@router.command(('query', 'q'), 'последние N запросов', 'N')  # /query
@command_arguments.digit(default=5)
async def _(message: Message, amount: int, queries_repo: QueriesRepository):
    queries = queries_repo.get_last_queries(int(amount))
    if not queries:
        await message.answer(PHRASES_RU.info.no_query)
        return

    txt = format_list.format_queries_text(
        queries=queries,
        footnote_template=PHRASES_RU.footnote.all_queries,
        line_template=PHRASES_RU.template.all_queries,
    )

    if txt:
        await message.answer(txt.replace('\t', '\n'), disable_web_page_preview=True)


@router.command('clear_temp', 'очистка временных файлов')  # /clear_temp
async def _(message: Message):
    if temp.clear():
        logger.info(f'TEMP directory cleared by user {message.from_user.id} ({message.from_user.username})')
        await message.answer(text=PHRASES_RU.success.clear_temp)
    else:
        await message.answer(text=PHRASES_RU.error.clear_temp)


@router.command(('user_query', 'uq', 'qu'), 'запросы пользователя по ID', 'user_id')  # /user_query
@command_arguments.user_id
async def _(message: Message, user_id: int, dialog_manager: DialogManager, **kwargs):
    queries_repo: QueriesRepository = await kwargs['dishka_container'].get(QueriesRepository)
    queries, _ = queries_repo.get_user_queries(user_id, 1, QUERIES_PER_PAGE)
    if not queries:
        await message.answer(PHRASES_RU.error.no_query)
        return
    await dialog_manager.start(UserQuerySG.list, data={'user_id': user_id}, mode=StartMode.NEW_STACK)


@router.command('test', 'отладка и тестирование функций')  # /test
async def _(message: Message):
    pass
