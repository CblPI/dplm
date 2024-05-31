from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


credit = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Посмотреть кредиты'),
        KeyboardButton('Удалить кредит'),
        KeyboardButton('Добавить кредит'),
        KeyboardButton('Начало'),
)

credit_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отмена')
)
