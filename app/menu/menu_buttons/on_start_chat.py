from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = [
        "on_start",
]


on_start = ReplyKeyboardMarkup(resize_keyboard=True).add(

        KeyboardButton('Расходы'),
        KeyboardButton('Доходы'),
        KeyboardButton('Кредиты'),
        KeyboardButton('Операции'),
        KeyboardButton('Цели'),
        KeyboardButton('Бюджет'),
        KeyboardButton('Инвестиции'),
        KeyboardButton('Счет'),
        KeyboardButton('Начало'),

)

