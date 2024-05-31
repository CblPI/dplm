from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

operations = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('get_operations_cat'),
        KeyboardButton('rm_operations_cat'),
        KeyboardButton('start'),
)
