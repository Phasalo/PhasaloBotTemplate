from aiogram import F
from DB.tables.users import UsersTable
from bot import keyboards
from bot.handlers.admin import command_getcmds
from aiogram.types import Message
from bot.bot_utils.routers import UserRouter, BaseRouter
from config import config
from phrases import PHRASES_RU

router = UserRouter()


@router.command('start', 'запустить бота')  # /start
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.start)


@router.command('help', 'как пользоваться ботом')  # /help
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.help)


@router.command('about', 'о разработчиках')  # /about
async def _(message: Message):
    await message.answer_photo(caption=PHRASES_RU.commands.about,
                               photo='https://yan-toples.ru/Phasalo/color-black-phasalo-project-margin.png',
                               disable_web_page_preview=True)


@router.command(('commands', 'cmds'), 'список всех команд (это сообщение)')  # /commands /cmds
async def _(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    await message.answer(PHRASES_RU.title.commands + commands_text)


@router.message(F.text == config.tg_bot.password)
async def _(message: Message):
    with UsersTable() as users_db:
        if users_db.set_admin(message.from_user.id, message.from_user.id):
            await message.delete()
            await message.answer(PHRASES_RU.success.promoted)
            await command_getcmds(message)
        else:
            await message.answer(PHRASES_RU.error.db)


@router.message()
async def _(message: Message):
    await message.answer(text=PHRASES_RU.answers.unknown, reply_markup=keyboards.default.keyboard)
