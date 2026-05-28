from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text.lower().in_(['спасибо', 'от души', 'благодарю']))
async def _(message: Message):
    await message.answer_sticker(sticker='CAACAgEAAxkBAAEKShplAfTsN4pzL4pB_yuGKGksXz2oywACZQEAAnY3dj9hlcwZRAnaOjAE')
