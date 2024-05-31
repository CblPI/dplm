from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = [
    'income'
]

income = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Посмотреть доходы'),
        KeyboardButton('Удалить доход'),
        KeyboardButton('Добавить доход'),
        KeyboardButton('Категории дохода'),
        KeyboardButton('Начало'),

)

income_category = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Посмотреть категории доходов'),
        KeyboardButton('Удалить категорию доходов'),
        KeyboardButton('Добавить категорию расходов'),
        KeyboardButton('Начало'),
)


income_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Отмена")
)
