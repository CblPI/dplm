from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

score = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Мои счета'),
        KeyboardButton('Добавить счет'),
        KeyboardButton('Удалить счет'),
        KeyboardButton('Начало'),
)

cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отмена')
)
