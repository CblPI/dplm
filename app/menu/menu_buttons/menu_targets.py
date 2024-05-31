
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

targets = ReplyKeyboardMarkup(resize_keyboard=True).add(

        KeyboardButton('get_targets_cat'),
        KeyboardButton('rm_targets_cat'),
        KeyboardButton('start'),


)