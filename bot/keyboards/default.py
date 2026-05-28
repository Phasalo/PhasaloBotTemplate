from aiogram.utils.keyboard import KeyboardButton as KButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup as KMarkup

from phrases import PHRASES_RU


def __make_placeholder_appeal() -> str:
    return PHRASES_RU.placeholder_appeal


button_1: KButton = KButton(text='Кнопка 1')
button_2: KButton = KButton(text='Кнопка 2')

keyboard: KMarkup = KMarkup(
    keyboard=[[button_1], [button_2]],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder=__make_placeholder_appeal(),
)
