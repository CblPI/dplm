
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

investment = ReplyKeyboardMarkup(resize_keyboard=True).add(

        KeyboardButton('get_investment_cat'),
        KeyboardButton('rm_investment_cat'),
        KeyboardButton('start'),


)