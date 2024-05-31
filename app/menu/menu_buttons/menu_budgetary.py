from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

budgetary = ReplyKeyboardMarkup(resize_keyboard=True).add(

        KeyboardButton('get_budgetary_cat'),
        KeyboardButton('rm_budgetary_cat'),
        KeyboardButton('expenses_category'),
        KeyboardButton('start'),
)