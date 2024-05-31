from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

expenses = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('get_exp_cat'),
        KeyboardButton('rm_exp_cat'),
        KeyboardButton('start'),
)
